from typing import List, Tuple
from midsearch.database import Document, Chunk
from langchain.text_splitter import MarkdownTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")
embeddings = OpenAIEmbeddings()


def count_tokens(text: str) -> int:
    return len(encoding.encode(text))


def create_document(id: str, chunks: List[str]) -> Tuple[Document, List[Chunk]]:
    document = Document(id=id)
    chunk_embeddings = []
    for chunk in chunks:
        chunk_embeddings.append(
            Chunk(doc_id=id, content=chunk, embedding=embeddings.embed_documents([chunk])[0]))
    return document, chunk_embeddings


def create_markdown_document(id: str, content: str) -> Tuple[Document, List[Chunk]]:
    splitter = MarkdownTextSplitter()
    chunks = splitter.split_text(content)
    return create_document(id=id, chunks=chunks)