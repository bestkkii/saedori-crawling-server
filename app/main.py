from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .api.v1.router import router as api_v1_router

# FastAPI 앱 생성
app = FastAPI(
    title="Saedori Crawling Server",
    description="크롤링 서버 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Gin 서버 주소
    allow_credentials=True,
    allow_methods=["GET"],  # GET 메서드만 허용
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Saedori Crawling Server is running"}

# 서버 실행
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # 모든 IP에서 접근 가능
        port=8000,
        reload=False,  # 프로덕션에서는 자동 리로드 비활성화
        workers=1  # 단일 워커 사용 (멀티프로세싱 없이 순차적 크롤링)
    )
