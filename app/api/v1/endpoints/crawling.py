
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import httpx
from ....config.settings import settings
from ....crawlers import get_crawler
from fastapi.responses import JSONResponse

router = APIRouter()   # main.py나 routes.py에 등록될 라우터


@router.post("/crawl/{site}")
async def crawl_site(site: str) -> Dict[str, Any]:
    """
    크롤링 요청을 받아서 크롤링 결과를 Gin에 전달한다.

    Args:
        site (str): 크롤링할 사이트 이름. google, music, ...
    Returns:
        Dict[str, Any]: 크롤링 결과 데이터. JSON 형식으로 Gin에 전달.
    """
    try:
        # 크롤러 가져오기
        crawler = get_crawler(site)
        # 등록되지 않은 이름이면 에러 반환
        if not crawler:
            raise HTTPException(status_code=400, detail=f"INVALID_PARAMETER: Crawler for {site} not found")

        # 크롤링 수행
        data = await crawler.crawl()

        # Gin 서버로 데이터 전송 (비동기 context manager 사용 시 안전하게 연결을 닫기 위해 async with 필요)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                ##### Gin에서 받을 Api path를 명시해야겠다!
                f"{settings.GIN_SERVER_URL}/api/v1/data/{site}",
                json=data
            )
            response.raise_for_status() # 응답 결과가 200(정상)이 아니면 에러 반환

        return_val = {"message": "Success", "result": {data}}
        return return_val

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error_code": "500", "message": "INTERNAL_SERVER_ERROR"}
        )