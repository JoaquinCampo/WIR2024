# Dockerfile
FROM python:3.9-slim

WORKDIR /backend/app

COPY ../app/requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ../app .
COPY ../docker/start.sh /backend/docker/start.sh

CMD ["/backend/docker/start.sh"]
