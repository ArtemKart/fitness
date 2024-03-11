FROM python:3.11.5-alpine

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .

RUN chmod a+x docker/*.sh

#ENV PATH="/code/docker:${PATH}"