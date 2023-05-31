set dotenv-load

export FLASK_DEBUG := "1"
export FLASK_APP := "midsearch.server"
export POSTGRES_URL := "postgresql://midsearch:midsearch_password@localhost:5432/midsearch"

stop-backend:
    docker-compose stop midsearch

stop-telegram-bot:
    #!/usr/bin/env bash
    if docker-compose ps --services | grep -q telegram-bot; then
        echo docker-compose stop telegram-bot;
    fi

stop-discord-bot:
    #!/usr/bin/env bash
    if docker-compose ps --services | grep -q discord-bot; then
        echo docker-compose stop discord-bot;
    fi

stop-slack-bot:
    #!/usr/bin/env bash
    if docker-compose ps --services | grep -q slack-bot; then
        echo docker-compose stop slack-bot;
    fi

debug-frontend:
    cd frontend && yarn dev

debug-backend: stop-backend
    flask run

debug-telegram-bot: stop-telegram-bot
    python3 midsearch/client telegram

debug-discord-bot: stop-discord-bot
    python3 midsearch/client discord

debug-slack-bot: stop-slack-bot
    python3 midsearch/client slack

debug-wechaty-bot:
    python3 midsearch/client wechaty

debug-mirai-bot:
    python3 midsearch/client mirai

debug-docs:
    sphinx-autobuild docs docs/_build/html
