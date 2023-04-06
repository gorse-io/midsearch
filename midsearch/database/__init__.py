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

from abc import ABC, abstractmethod
from typing import List

from midsearch.document import Document


class Database(ABC):

    @abstractmethod
    def upsert_document(self, document: Document):
        pass

    @abstractmethod
    def delete_document(self, name: str):
        pass

    @abstractmethod
    def search_documents(self, query: str) -> List[Document]:
        pass
