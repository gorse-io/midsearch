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


embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory='conchdb/data', embedding_function=embeddings)
retriever = VectorStoreRetriever(vectorstore=db)
qa = RetrievalQA.from_llm(llm=ChatOpenAI(temperature=0.1), retriever=retriever)


app = Flask(__name__)


@app.route("/api/search/")
def search():
    query = request.args.get('query')
    docs = retriever.get_relevant_documents(query)
    results = []
    for doc in docs:
        results.append({
            'page_content': mistune.html(doc.page_content),
            'metadata': doc.metadata,
        })
    return jsonify(results)


@app.route("/api/chat/")
def chat():
    message = request.args.get('message')
    return mistune.html(qa.run(message))
