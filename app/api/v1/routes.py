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
from .endpoints import crawling

router = APIRouter()
router.include_router(crawling.router, prefix="/crawling")

# 채은, 가경 commit 감사합니다. 크롤링은 endpoints를 따로 만들어서 아래는 수정 예정!
from app.services.data_service import music_service, realtime_search_words_service

# Music
@router.get("/crawl/music")
def music():
    return music_service()

# Realtime Search Words
@router.get("/crawl/realtime-search-words")
def realtime_search_words():
    return realtime_search_words_service()
