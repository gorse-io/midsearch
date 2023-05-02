#######################
# STEP 1 build frontend
#######################
FROM node:19

COPY ./frontend /frontend

WORKDIR /frontend

RUN yarn install && yarn build

#################################
# STEP 2 setup python environment
#################################
FROM python:3.11

COPY ./midsearch /midsearch

COPY --from=0 /frontend/dist /midsearch/static

COPY requirements.txt /

WORKDIR /

RUN pip install -r requirements.txt

CMD waitress-serve --host 0.0.0.0 --port 8080 midsearch:app
