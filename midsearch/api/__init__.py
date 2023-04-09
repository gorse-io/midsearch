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

import openai
import numpy as np
from flask import Flask, abort, request
from midsearch.database import PGVector
from midsearch.document import Document

app = Flask(__name__)
db = PGVector(
    'postgresql://midsearch:midsearch_password@localhost:5432/midsearch')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/docs", methods=["GET"])
def get_docs():
    n = request.args.get('n', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    documents = db.get_documents(n, offset)
    return documents


@app.route("/doc", methods=["POST"])
def post_doc():
    document = request.get_json()
    db.upsert_document(Document(
        name=document['name'],
        content=document['content'],
    ))
    return {'row_affected': 1}


@app.route("/doc/<doc_id>", methods=["GET"])
def get_doc(doc_id):
    document = db.get_document(doc_id)
    if document is None:
        abort(404)
    return document


@app.route("/doc/<doc_id>", methods=["DELETE"])
def delete_doc(doc_id):
    db.delete_document(doc_id)
    return {'row_affected': 1}


@app.route("/search/<query>", methods=["GET"])
def search(query):
    embedding = np.array(openai.Embedding.create(
        input=[query], model='text-embedding-ada-002')['data'][0]['embedding'])
    documents = db.search_documents(embedding, 1)
    for d in documents:
        print(d.name, d.content)
    return []
