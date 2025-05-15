FROM python:3.10.12-slim-bullseye
WORKDIR /app
COPY get_secret.py requirements.txt /app/
RUN pip3 install -r requirements.txt