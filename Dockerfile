FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 33333

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "33333"]
