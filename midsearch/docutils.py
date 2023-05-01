import hashlib
from typing import List, Tuple

import tiktoken
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import MarkdownTextSplitter

from midsearch.database import Document, Chunk

encoding = tiktoken.get_encoding("cl100k_base")
embeddings = OpenAIEmbeddings()


def count_tokens(text: str) -> int:
    return len(encoding.encode(text))


def create_document(id: str, md5: str, chunks: List[str]) -> Tuple[Document, List[Chunk]]:
    document = Document(id=id, md5=md5)
    chunk_embeddings = []
    for chunk in chunks:
        chunk_embeddings.append(
            Chunk(doc_id=id, content=chunk, embedding=embeddings.embed_documents([chunk])[0]))
    return document, chunk_embeddings


def create_markdown_document(id: str, content: str) -> Tuple[Document, List[Chunk]]:
    md5 = hashlib.md5(content.encode('utf-8')).hexdigest()
    splitter = MarkdownTextSplitter()
    chunks = splitter.split_text(content)
    return create_document(id=id, md5=md5, chunks=chunks)
