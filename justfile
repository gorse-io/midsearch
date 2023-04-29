export FLASK_DEBUG := "1"
export FLASK_APP := "midsearch"
export POSTGRES_URL := "postgresql://midsearch:midsearch_password@localhost:5432/midsearch"

debug-frontend:
    cd frontend && yarn dev

debug-backend:
    flask run
