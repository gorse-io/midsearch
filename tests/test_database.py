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

import unittest
import os
import numpy as np
from midsearch.document import Document
from midsearch.database import PGVector


class TestPGVector(unittest.TestCase):

    def setUp(self):
        url = os.getenv(
            'POSTGRES_URL', 'postgresql://midsearch:midsearch_password@localhost:5432/midsearch')
        self.database = PGVector(url)

    def tearDown(self):
        pass

    def test_crud(self):
        # upsert document
        self.database.upsert_document(
            Document('alice', 'Alice in Wonderland', np.zeros(1536)))
        # get document
        document = self.database.get_document('alice')
        self.assertEqual(document.name, 'alice')
        self.assertEqual(document.content, 'Alice in Wonderland')
        self.assertTrue(np.array_equal(document.embedding(), np.zeros(1536)))
        # delete document
        self.database.delete_document('alice')
        document = self.database.get_document('alice')
        self.assertIsNone(document)

    def test_search(self):
        # upsert documents
        self.database.upsert_document(
            Document('alice', 'Alice in Wonderland', np.ones(1536)))
        self.database.upsert_document(
            Document('bob', 'Bob in Wonderland', np.ones(1536) * 2))
        self.database.upsert_document(
            Document('carol', 'Carol in Wonderland', np.ones(1536) * 3))
        self.database.upsert_document(
            Document('david', 'David in Wonderland', np.ones(1536) * 4))
        self.database.upsert_document(
            Document('eve', 'Eve in Wonderland', np.ones(1536) * 5))
        # search documents
        documents = self.database.search_documents(np.zeros(1536), 3)
        self.assertEqual(len(documents), 3)
        self.assertEqual(documents[0].name, 'alice')
        self.assertEqual(documents[1].name, 'bob')
        self.assertEqual(documents[2].name, 'carol')
        documents = self.database.search_documents(np.ones(1536) * 6, 3)
        self.assertEqual(len(documents), 3)
        self.assertEqual(documents[0].name, 'eve')
        self.assertEqual(documents[1].name, 'david')
        self.assertEqual(documents[2].name, 'carol')


if __name__ == '__main__':
    unittest.main()
