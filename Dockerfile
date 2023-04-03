# syntax=docker/dockerfile:1
FROM python:3.10.6

WORKDIR /DTF_APP

COPY requirements.txt requirements.txt
COPY ./DTF_APP /DTF_APP

RUN pip install -r requirements.txt

CMD [ "uvicorn", "main:serv",  "--host", "0.0.0.0", "--port", "37000" ]