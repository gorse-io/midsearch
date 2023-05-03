# Copyright 2023 MidSearch Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import os
from functools import wraps

import mistune
import openai.error
from flask import Flask, jsonify, request, make_response
from flask_login import LoginManager, UserMixin, login_user
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain

from midsearch.database import PGVector, Conversation
from midsearch.docutils import create_markdown_document, count_tokens

# Load gloabl config
MAX_CONTEXT_LENGTH = int(os.getenv('MIDSEARCH_MAX_CONTEXT_LENGTH', 4096))
USERNAME = os.getenv('MIDSEARCH_USERNAME')
PASSWORD = os.getenv('MIDSEARCH_PASSWORD')
API_KEY = os.getenv('MIDSEARCH_API_KEY')


def key_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = ''
        if 'X-Api-Key' in request.headers:
            token = request.headers['X-Api-Key']
        if API_KEY != '' and token != API_KEY:
            return make_response('invalid api key', 401)
        return f(*args, **kwargs)
    return decorator


pg = PGVector(os.environ['POSTGRES_URL'])

app = Flask(__name__, static_folder="./static", static_url_path="/")


# Add error handlers

@app.errorhandler(openai.error.InvalidRequestError)
def handle_invalid_request(e):
    return str(e), 500


app.register_error_handler(400, handle_invalid_request)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if user_id == os.getenv('MIDSEARCH_USERNAME'):
        return UserMixin()
    return None


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == os.getenv('MIDSEARCH_USERNAME') and password == os.getenv('MIDSEARCH_PASSWORD'):
        user = UserMixin()
        login_user(user)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route("/api/search/")
def search():
    query = request.args.get('query')
    chunks = pg.search_documents(query)
    results = []
    for chunk, score in chunks:
        results.append({
            'page_content': mistune.html(chunk.content),
            'token_count': count_tokens(chunk.content),
            'score': score,
        })
    return jsonify(results)


@app.route("/api/chat/")
@key_required
def chat():
    # Get question
    question = request.args.get('message')
    # Get accept MIME type
    mime_type = request.accept_mimetypes.best_match(
        ['text/html', 'text/markdown'])
    # Search revelevant documents
    chunks = pg.search_documents(question)
    prompt = ''.join([chunk.content for chunk, _ in chunks])
    docs = []
    length = 0
    for chunk, _ in chunks:
        token_count = count_tokens(chunk.content)
        if length + token_count > MAX_CONTEXT_LENGTH:
            break
        docs.append(Document(page_content=chunk.content))
        length += token_count
    # Create prompt
    chat = ChatOpenAI()
    chain = load_qa_chain(chat, chain_type="stuff")
    answer = chain.run(input_documents=docs, question=question)
    pg.add_conversation(Conversation(
        question=question, answer=answer, prompt=prompt))
    # Render answer
    if mime_type == 'text/markdown':
        return answer
    elif mime_type == 'text/html':
        return mistune.html(answer)
    else:
        return f"unsupported accept MIME type: {mime_type}", 400


@app.route("/api/conversations/", methods=['GET'])
def get_conversations():
    offset = request.args.get('offset', 0)
    n = request.args.get('n', 10)
    conversations = pg.get_conversations(offset=offset, n=n)
    return jsonify([{
        'id': conversation.id,
        'question': conversation.question,
        'answer': mistune.html(conversation.answer),
        'prompt': mistune.html(conversation.prompt),
        'helpful': conversation.helpful,
        'timestamp': conversation.timestamp,
    } for conversation in conversations])


@app.route("/api/conversations/count/", methods=['GET'])
def count_conversations():
    return jsonify(pg.count_conversations())


@app.route("/api/conversation/<id>", methods=['POST'])
def update_conversation(id: int):
    helpful = request.form.get('helpful')
    pg.update_conversation(id=id, helpful=(helpful == 'true'))
    return jsonify({'success': True})


@app.route("/api/conversation/<id>", methods=['DELETE'])
def delete_conversation(id: int):
    pg.delete_conversation(id=id)
    return jsonify({'success': True})


@app.route("/api/documents/count/", methods=['GET'])
def count_documents():
    return jsonify(pg.count_documents())


@app.route("/api/documents/", methods=['GET'])
def get_documents():
    offset = request.args.get('offset', 0)
    n = request.args.get('n', 10)
    documents = pg.get_documents(offset=offset, n=n)
    return jsonify([{
        'id': document[0].id,
        'updated_at': document[0].updated_at,
        'chunks': [{
            'content': mistune.html(chunk.content),
            'token_count': count_tokens(chunk.content),
        } for chunk in document[1]],
    } for document in documents])


@app.route("/api/document/<string:id>", methods=['POST'])
def update_document(id: str):
    content = request.form.get('content')
    # check if document exists
    exists = pg.get_document(id)
    if exists:
        md5 = hashlib.md5(content.encode('utf-8')).hexdigest()
        if exists.md5 == md5:
            return jsonify({'success': True})
    # create document if it doesn't exist
    document = create_markdown_document(id, content)
    pg.add_document(document)
    return jsonify({'success': True})
