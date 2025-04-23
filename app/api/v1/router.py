from fastapi import APIRouter
from .endpoints import crawling

# API 버전 1 라우터 생성
router = APIRouter()

# 크롤링 엔드포인트 등록
router.include_router(crawling.router, tags=["crawling"])
