# Gin에서 크롤링 요청 받기 /api/????
## 크롤링 수행하기
## 데이터를 json 형식으로 변환
## 데이터를 Gin에 전달

# from fastapi import APIRouter

# router = APIRouter()

# @router.post("/crawl")
# async def crawl_data(request: CrawlRequest):
#     # 크롤링 수행
#     # 데이터를 json 형식으로 변환
#     # 데이터를 Gin에 전달
#     return {"message": "Crawling completed"}

from fastapi import APIRouter
from app.services.data_service import music_service

router = APIRouter()

# Music
@router.get("/crawl/music")
def music():
    return music_service()