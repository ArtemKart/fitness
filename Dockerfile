FROM python:3.11

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .
