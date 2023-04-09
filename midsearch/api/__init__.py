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

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/docs", methods=["GET"])
def get_docs():
    return "<p>Documents</p>"


@app.route("/docs", methods=["POST"])
def post_docs():
    return "<p>Document</p>"


@app.route("/doc/<doc_id>", methods=["GET"])
def get_doc(doc_id):
    return f"<p>Document {doc_id}</p>"
