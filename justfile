set dotenv-load

export FLASK_DEBUG := "1"
export FLASK_APP := "midsearch"
export POSTGRES_URL := "postgresql://midsearch:midsearch_password@localhost:5432/midsearch"

stop-backend:
    docker-compose stop midsearch

debug-frontend:
    cd frontend && yarn dev

debug-backend: stop-backend
    flask run

debug-telegram:
    python3 midsearch telegram

debug-discord:
    python3 midsearch discord
