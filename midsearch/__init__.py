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

from flask import Flask, jsonify, request
from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import mistune
from midsearch.database import PGVector, Conversation
import os
from midsearch.docutils import create_markdown_document, count_tokens
from langchain.prompts import load_prompt
from langchain.schema import HumanMessage


pg = PGVector(os.environ['POSTGRES_URL'])

app = Flask(__name__)


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
def chat():
    question = request.args.get('message')
    # Search revelevant documents
    chunks = pg.search_documents(question)
    context = '\n\n'.join([chunk.content for chunk, _ in chunks])
    # Create prompt
    template = load_prompt('lc://prompts/qa/stuff/basic.yaml')
    prompt = template.format(context=context, question=question)
    chat = ChatOpenAI(temperature=0)
    answer = chat([HumanMessage(content=prompt)]).content
    pg.add_conversation(Conversation(question=question, answer=answer))
    return mistune.html(answer)


@app.route("/api/conversations/", methods=['GET'])
def get_conversations():
    offset = request.args.get('offset', 0)
    n = request.args.get('n', 10)
    conversations = pg.get_conversations(offset=offset, n=n)
    return jsonify([{
        'id': conversation.id,
        'question': conversation.question,
        'answer': mistune.html(conversation.answer),
        'promppt': conversation.promppt,
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
    document = create_markdown_document(id, content)
    pg.add_document(document)
    return jsonify({'success': True})
