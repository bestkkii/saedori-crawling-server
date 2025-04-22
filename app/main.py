from fastapi import FastAPI
from .config.settings import settings
from .api.v1.routes import router as api_v1_router
import uvicorn

# 웹서버 실행
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"  # 웹서버 실행 시 자동으로 생성되는 OpenAPI Swagger 문서의 경로
)

# API 라우터 등록
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Crawling Service API"} # 서버 접속 확인 용 return값

# 서버 실행
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
