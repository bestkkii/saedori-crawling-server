# Gin에서 크롤링 요청 받기 /api/????
## 크롤링 수행하기
## DB에 저장

# Gin에서 데이터 POST 받기 API 명세서에 따라 /api/v1/...
## DB에서 데이터 조회
## Gin에 전달

from fastapi import APIRouter
from app.services.data_service import music_service

router = APIRouter()

# Music
@router.get("/crawl/music")
def music():
    return music_service()