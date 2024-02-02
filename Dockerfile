FROM python:3.12.1-alpine3.19
COPY . /app

WORKDIR /app
RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT gunicorn main:app --worker-class aiohttp.GunicornWebWorker --bind 0.0.0.0:8000