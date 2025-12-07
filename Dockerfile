FROM python:3.13-slim

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN chmod +x /wait-for-it.sh

COPY ./app /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 33333

# CMD를 wait-for-it로 감싸서 DB와 Redis 준비 후 실행
CMD ["/wait-for-it.sh", "mysql:3306", "--", "/wait-for-it.sh", "redis:6379", "--", "python", "-m", "app.main"]
