FROM python:3.9.6-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /app/data

ENV PRODUCTION=true

EXPOSE 5001

CMD ["gunicorn","--bind","0.0.0.0:5001","app:app"]
