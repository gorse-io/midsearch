#######################
# STEP 1 build frontend
#######################
FROM node:19

COPY ./frontend /frontend

WORKDIR /frontend

RUN yarn install && yarn build

# FROM python:3.11

# # Install dependencies
# RUN pip install -r requirements.txt
