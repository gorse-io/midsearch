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

import numpy as np
import openai
from typing import List, Optional


class Document:

    def __init__(self, name: str, content: str, embedding: Optional[np.ndarray] = None):
        self.name = name
        self.content = content
        self._embedding = embedding

    def embedding(self) -> np.ndarray:
        if self._embedding is None:
            if len(self.content) == 0:
                raise ValueError('Empty content')
            self._embedding = np.array(openai.Embedding.create(
                input=[self.content], model='text-embedding-ada-002')['data'][0]['embedding'])
        return self._embedding
