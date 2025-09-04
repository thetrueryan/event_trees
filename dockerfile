FROM python:3.12.3-slim

WORKDIR /events_app

COPY requirements.txt .

RUN pip install -r requirements.txt