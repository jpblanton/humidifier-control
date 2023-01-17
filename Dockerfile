FROM python:3.10.5-bullseye

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .