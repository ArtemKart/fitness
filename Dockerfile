FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY /src /code/src

#CMD [ "python", "src/main.py" ]
#CMD ["uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"]