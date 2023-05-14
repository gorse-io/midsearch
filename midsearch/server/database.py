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

import datetime
from typing import List, Tuple

import numpy as np
import sqlalchemy
from langchain.embeddings.openai import OpenAIEmbeddings
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import declarative_base, Session

embeddings = OpenAIEmbeddings()

Base = declarative_base()


class Document(Base):
    __tablename__ = "document"

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    md5 = sqlalchemy.Column(sqlalchemy.String)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.utcnow)


class Chunk(Base):
    __tablename__ = "chunk"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    doc_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(
        "document.id", ondelete="CASCADE", deferrable=True), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String)
    embedding = sqlalchemy.Column(Vector(1536))


class Conversation(Base):
    __tablename__ = "conversation"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    prompt = sqlalchemy.Column(sqlalchemy.String)
    helpful = sqlalchemy.Column(sqlalchemy.Boolean)
    user_agent = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.String)
    timestamp = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.utcnow)


class PGVector:

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

    def add_document(self, document: Tuple[Document, List[Chunk]]):
        with Session(self.engine) as session:
            session.execute(sqlalchemy.text('SET CONSTRAINTS ALL DEFERRED'))
            # delete existing document
            session.query(Document).filter_by(id=document[0].id).delete()
            # insert new document
            session.add(document[0])
            session.add_all(document[1])
            session.commit()

    def delete_document(self, id: str):
        with Session(self.engine) as session:
            session.query(Document).filter_by(id=id).delete()
            session.commit()

    def get_documents(self, n: int, offset: int = 0) -> List[Tuple[Document, List[Chunk]]]:
        with Session(self.engine) as session:
            documents = session.query(Document).limit(n).offset(offset).all()
            results = []
            for document in documents:
                chunks = session.query(Chunk).filter_by(
                    doc_id=document.id).all()
                results.append((document, chunks))
            return results

    def get_document(self, id: str) -> Document:
        with Session(self.engine) as session:
            return session.query(Document).filter_by(id=id).first()

    def count_documents(self) -> int:
        with Session(self.engine) as session:
            return session.query(Document).count()

    def search_documents(self, query: str, k: int = 5) -> List[Chunk]:
        with Session(self.engine) as session:
            embedding = np.asarray(embeddings.embed_query(query))
            return session.query(Chunk, Chunk.embedding.l2_distance(embedding).label("distance")).order_by(
                sqlalchemy.asc("distance")).limit(k).all()

    def add_conversation(self, conversation: Conversation) -> int:
        with Session(self.engine) as session:
            session.add(conversation)
            session.commit()
            return conversation.id

    def get_conversations(self, n: int, offset: int = 0) -> List[Conversation]:
        with Session(self.engine) as session:
            return session.query(Conversation).order_by(Conversation.id.desc()).limit(
                n).offset(offset).all()

    def update_conversation(self, id: int, helpful: bool):
        with Session(self.engine) as session:
            session.query(Conversation).filter_by(id=id).update(
                {Conversation.helpful: helpful})
            session.commit()

    def delete_conversation(self, id: int):
        with Session(self.engine) as session:
            session.query(Conversation).filter_by(id=id).delete()
            session.commit()

    def count_conversations(self) -> int:
        with Session(self.engine) as session:
            return session.query(Conversation).count()

    def get_conversations_quality(self, begin_date: datetime.date, end_date: datetime.date) -> Tuple[List[datetime.date], List[int], List[int], List[int]]:
        with Session(self.engine) as session:
            rows = session.execute(sqlalchemy.text('select date(timestamp), helpful, count(*) from conversation where date(timestamp) >= :begin_date and date(timestamp) <= :end_date group by date(timestamp), helpful'),
                                   {"begin_date": begin_date, "end_date": end_date}).fetchall()
            count = {}
            for row in rows:
                count[(row[0], row[1])] = row[2]
            quality = [], [], [], []
            for date in range((end_date - begin_date).days + 1):
                date = begin_date + datetime.timedelta(days=date)
                quality[0].append(date.strftime("%Y-%m-%d"))
                for idx, helpful in enumerate([True, False, None]):
                    quality[idx + 1].append(count.get((date, helpful), 0))
            return quality
