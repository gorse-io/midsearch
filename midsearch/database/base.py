from abc import ABC, abstractmethod
from midsearch.document import Document
from typing import List, Optional
import numpy as np


class Database(ABC):

    @abstractmethod
    def upsert_document(self, document: Document):
        pass

    @abstractmethod
    def delete_document(self, name: str):
        pass

    @abstractmethod
    def get_document(self, name: str) -> Optional[Document]:
        pass

    @abstractmethod
    def search_documents(self, embedding: np.ndarray) -> List[Document]:
        pass
