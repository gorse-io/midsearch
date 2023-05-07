# MidSearch

<p align="center">
<img width=400 src="./assets/midsearch.png">
</p>

[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/zhenghaoz/midsearch)](https://hub.docker.com/r/zhenghaoz/midsearch)
[![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/zhenghaoz/midsearch)](https://hub.docker.com/r/zhenghaoz/midsearch)
[![Docker Pulls](https://img.shields.io/docker/pulls/zhenghaoz/midsearch)](https://hub.docker.com/r/zhenghaoz/midsearch)

MidSearch is a middleware to connect chat bots to search engines. It gerenetes human friendly answers to user questions based on ingested documents. Besides its basic question answering ability, MidSearch also supports more advanced features:

- **Observality**: Conversactions between users and chat bots are recorded and can be used to improve documents.
- **Evaluation**: Users or administrators can rate the quality of answers to questions to track the quality of documents.
- **Multi-platform**: MidSearch can be used by chat bots on different platforms, such as Telegram, Discord, etc.

## Deployment

1. Clone the repository:

```bash
git clone git@github.com:gorse-io/midsearch.git
cd midsearch
```

2. Create a `.env` file in the root directory of the project:

```bash
# OpenAI API Key
OPENAI_API_KEY=sk-xxxxxxxx

# MidSearch API Key
MIDSEARCH_API_KEY=xxxxxxxx
```

3. Start the MidSearch stack:

```bash
docker-compose up -d
```

## Usage

### Ingest Documents

### Setup Telegram Bot

1. [Create a Telegram bot](https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot) and paste the bot token in the `.env` file:

```bash
# Telegram Bot Token
TELEGRAM_BOT_TOKEN=xxxxxxxx
```

2. Start the Telegram bot:

```bash
docker-compose up -d
```

### Setup Discord Bot

1. [Create a Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html) and paste the bot token in the `.env` file:

```bash
# Discord Bot Token
DISCORD_BOT_TOKEN=xxxxxxxx
```

2. Start the Discord bot:

```bash
docker-compose up -d
```

## Acknowledgments

MidSearch is inspired by the following projects:

- [LangChain](https://github.com/hwchase17/langchain)
- [LlamaIndex](https://github.com/jerryjliu/llama_index)
