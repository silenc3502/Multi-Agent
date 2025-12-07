FROM python:3.13-slim

COPY ./app /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 33333

CMD ["python", "-m", "app.main"]