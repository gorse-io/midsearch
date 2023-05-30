Documents Ingestion
===================

GitHub Action
-------------

.. code-block:: yaml

    name: sync

    on:
    push:
        branches:    
        - main

    jobs:
    midsearch:
        name: midsearch
        runs-on: ubuntu-latest
        steps:
        - name: Checkout
            uses: actions/checkout@v3
        - name: Set up Python
            uses: actions/setup-python@v4
        - name: Install dependencies
            run: pip install git+https://github.com/gorse-io/midsearch.git
        - name: Sync to Midsearch
            run: midsearch sync src/docs/master
            env:
            MIDSEARCH_ENDPOINT: ${{ secrets.MIDSEARCH_ENDPOINT }}
            MIDSEARCH_API_KEY: ${{ secrets.MIDSEARCH_API_KEY }}
