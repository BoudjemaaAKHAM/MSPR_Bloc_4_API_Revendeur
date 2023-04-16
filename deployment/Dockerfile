FROM python:3.10-alpine

WORKDIR /app

RUN pip install --upgrade pip

COPY data ../data
COPY database database
COPY revendeurapi revendeurapi
COPY services services
COPY ssl ssl
COPY utilities utilities

COPY setup.py setup.py

RUN pip install -e .


EXPOSE 82
EXPOSE 444

CMD ["uvicorn", "revendeurapi.main:app", "--host", "0.0.0.0", "--port", "444", "--ssl-keyfile", "/app/ssl/key.pem", "--ssl-certfile", "/app/ssl/cert.pem"]