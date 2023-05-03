set dotenv-load

export FLASK_DEBUG := "1"
export FLASK_APP := "midsearch"
export POSTGRES_URL := "postgresql://midsearch:midsearch_password@localhost:5432/midsearch"

stop-backend:
    docker-compose stop midsearch

stop-telegram-bot:
    docker-compose stop telegram-bot

stop-discord-bot:
    docker-compose stop discord-bot

debug-frontend:
    cd frontend && yarn dev

debug-backend: stop-backend
    flask run

debug-telegram-bot: stop-telegram-bot
    python3 midsearch telegram

debug-discord-bot: stop-discord-bot
    python3 midsearch discord
