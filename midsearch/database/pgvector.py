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

from midsearch.database.base import Database
from midsearch.document import Document
from typing import List, Optional
import numpy as np
import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from pgvector.sqlalchemy import Vector


Base = declarative_base()


class DocumentEmbedding(Base):
    __tablename__ = "document_embedding"

    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    content = sqlalchemy.Column(sqlalchemy.String)
    embedding = sqlalchemy.Column(Vector(1536))


class PGVector(Database):

    def __init__(self, url: str):
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()
        # create extension if not exists
        with Session(self.connection) as session:
            statement = sqlalchemy.text(
                "CREATE EXTENSION IF NOT EXISTS vector")
            session.execute(statement)
            session.commit()
        # create tables if not exists
        Base.metadata.create_all(self.engine)

    def upsert_document(self, document: Document):
        with Session(self.engine) as session:
            session.merge(DocumentEmbedding(
                name=document.name,
                content=document.content,
                embedding=document.embedding(),
            ))
            session.commit()

    def delete_document(self, name: str):
        with Session(self.engine) as session:
            session.query(DocumentEmbedding).filter_by(name=name).delete()
            session.commit()

    def get_document(self, name: str) -> Optional[Document]:
        with Session(self.engine) as session:
            document = session.query(DocumentEmbedding).get(name)
            if document is None:
                return None
            return Document(
                name=document.name,
                content=document.content,
                embedding=document.embedding,
            )

    def search_documents(self, embedding: np.ndarray, k: int) -> List[Document]:
        with Session(self.engine) as session:
            results = session.query(DocumentEmbedding, DocumentEmbedding.embedding.l2_distance(embedding).label("distance")).order_by(
                sqlalchemy.asc("distance")).limit(k).all()
            return [
                Document(
                    name=results.DocumentEmbedding.name,
                    content=results.DocumentEmbedding.content,
                    embedding=results.DocumentEmbedding.embedding,
                )
                for results in results
            ]
