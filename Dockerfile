FROM python:3.13-slim

# 컨테이너 작업 디렉토리
WORKDIR /app

# requirements 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사 (모든 도메인 포함)
COPY . .

# PYTHONPATH 지정 (루트 전체)
ENV PYTHONPATH=/app

EXPOSE 33333

CMD ["python", "-m", "app.main"]
