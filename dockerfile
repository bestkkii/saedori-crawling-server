# 1. 빌드 스테이지 (필수는 아니지만, 빌드시 패키지 캐싱에 유리)
FROM python:3.12-slim AS builder

# 시스템 패키지 설치 (필요하다면)
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# 작업 디렉토리 생성
WORKDIR /app

# 의존성 파일 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --user -r requirements.txt

# 소스 코드 복사
COPY . .

# 2. 실행 스테이지 (경량)
FROM python:3.12-slim

WORKDIR /app

# 의존성 복사
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 소스 복사
COPY . .

# 포트 노출 (FastAPI 기본: 8000)
EXPOSE 8000

# 실행 명령 (app.main:app은 FastAPI 인스턴스 위치에 맞게 수정)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]