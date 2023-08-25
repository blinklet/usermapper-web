FROM python:alpine
EXPOSE 8080
WORKDIR /app
COPY . .
RUN apk update && \
    apk add git && \
    pip install --no-cache-dir -r requirements.txt && \
    mkdir ./downloads
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "application:app"]