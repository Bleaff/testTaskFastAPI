# syntax=docker/dockerfile:1
FROM python:3.10.6
WORKDIR /code
ENV FASTAPI_APP=main.py
ENV DTF_RUN_HOST=0.0.0.0
ENV DTF_RUN_PORT=37000
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]