from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ....services.data_service import data_service

# 크롤링 라우터 생성
router = APIRouter()

@router.get("/crawl", response_model=Dict[str, Any])
def crawl():
    """
    모든 크롤러를 실행하고 결과를 반환하는 엔드포인트
    
    Returns:
        Dict[str, Any]: 크롤링 결과
        {
            "message": "Success",
            "created_at": 1735689600,
            "music_crawl": {
                "crawling": "Success",
                "result": {...}
            },
            "news_crawl": {
                "crawling": "Success",
                "result": {...}
            },
            "realtime_search_words_crawl": {
                "crawling": "Success",
                "result": {...}
            }
        }
    """
    try:
        # data_service를 통해 크롤링 실행
        results = data_service.crawl_all()
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "500",
                "message": "INTERNAL_SERVER_ERROR",
                "detail": str(e)
            }
        )