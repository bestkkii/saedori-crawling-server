from abc import ABC, abstractmethod
import aiohttp # 비동기 http 요청 처리
from ..config.settings import settings

class BaseCrawler(ABC):
    def __init__(self):
        self.headers = {
            "User-Agent": settings.USER_AGENT
        }
        self.timeout = settings.CRAWLING_TIMEOUT

    async def fetch(self, url: str) -> str:
        """
        비동기로 http 요청 보내기

        Args:
            url (str): 크롤링할 URL
        Returns:
            (str): HTML 문자열
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, timeout=self.timeout) as response:
                return await response.text()

    @abstractmethod
    async def crawl(self) -> dict:
        """
        크롤링을 수행하고 결과를 반환하는 메서드
        Returns:
            dict: 크롤링 결과 데이터. Gin에게 전달할 JSON 형식.
        """
        pass
