FROM python:3.10-alpine

WORKDIR /app

RUN pip install --upgrade pip

COPY ssl ssl
COPY setup.py setup.py

RUN pip install -e .

# copy only the api folder to the container
COPY revendeurapi revendeurapi

EXPOSE 82
EXPOSE 444

CMD ["uvicorn", "revendeurapi.main:app", "--host", "0.0.0.0", "--port", "444", "--ssl-keyfile", "/app/ssl/key.pem", "--ssl-certfile", "/app/ssl/cert.pem"]