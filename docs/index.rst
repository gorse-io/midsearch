.. midsearch documentation master file, created by
   sphinx-quickstart on Sun May 21 20:11:49 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MidSearch's documentation!
=====================================

MidSearch is a middleware to connect chat bots to documents search (powered by Postgres). It gerenetes human friendly answers to user questions based on ingested documents. Besides its basic question answering ability, MidSearch also supports more advanced features:

- **Observality:** Conversactions between users and chat bots are recorded and can be used to improve documents.
- **Evaluation:** Users or administrators can rate the quality of answers to questions to track the quality of documents.
- **Multi-platform:** MidSearch can be used by chat bots on different platforms, such as Telegram, Discord, etc.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   ingestion
   bot
