Bot Integration
===============

Telegram Bot
------------

1. `Create a Telegram bot <https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot>`_ and paste the bot token in the .env file:

.. code-block:: dot

    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN=xxxxxxxx

2. Uncomment the following lines in the docker-compose.yml file:

.. code-block:: yaml

  telegram-bot:
    build: zhenghaoz/midsearch
    environment:
      MIDSEARCH_ENDPOINT: http://midsearch:8080/api/
      MIDSEARCH_API_KEY: ${MIDSEARCH_API_KEY}
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
    command: python3 midsearch/client telegram

3. Start the Telegram bot:

.. code-block:: bash

    docker-compose up -d

Discord Bot
-----------

1. `Create a Discord bot <https://discordpy.readthedocs.io/en/stable/discord.html>`_ and paste the bot token in the .env file:

.. code-block:: dot

    # Discord Bot Token
    DISCORD_BOT_TOKEN=xxxxxxxx


2. Uncomment the following lines in the docker-compose.yml file:

.. code-block:: yaml

  discord-bot:
    build: zhenghaoz/midsearch
    environment:
      MIDSEARCH_ENDPOINT: http://midsearch:8080/api/
      MIDSEARCH_API_KEY: ${MIDSEARCH_API_KEY}
      DISCORD_BOT_TOKEN: ${DISCORD_BOT_TOKEN}
    command: python3 midsearch/client discord

3. Start the Discord bot:

.. code-block:: bash

    docker-compose up -d

Slack Bot
---------

1. `Create a Slack bot <https://www.pragnakalp.com/create-slack-bot-using-python-tutorial-with-examples/>`_ and paste the bot token in the .env file:

.. code-block:: dot

    # Slack Bot Token
    SLACK_BOT_TOKEN=xxxxxxxx

2. Uncomment the following lines in the docker-compose.yml file:

.. code-block:: yaml

  discord-bot:
    build: zhenghaoz/midsearch
    environment:
      MIDSEARCH_ENDPOINT: http://midsearch:8080/api/
      MIDSEARCH_API_KEY: ${MIDSEARCH_API_KEY}
      SLACK_BOT_TOKEN: ${SLACK_BOT_TOKEN}
    command: python3 midsearch/client slack

3. Start the Slack bot:

.. code-block:: bash

    docker-compose up -d

Wechat Bot (Wechaty)
--------------------

QQ Bot (Mirai)
--------------
