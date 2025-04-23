from typing import Dict, Type
from .base import BaseCrawler

# 크롤러 등록을 위한 딕셔너리
_crawlers: Dict[str, Type[BaseCrawler]] = {}

def register_crawler(name: str, crawler_class: Type[BaseCrawler]):
    """
    크롤러를 등록하는 함수
    
    Args:
        name (str): 크롤러 이름
        crawler_class (Type[BaseCrawler]): 크롤러 클래스

    Example:
        @ 각 크롤러 파일에서
        register_crawler("google", GoogleCrawler)
    """
    _crawlers[name] = crawler_class

def get_crawler(name: str) -> Type[BaseCrawler]:
    """
    등록된 크롤러를 가져오는 함수

    Args:
        name (str): 크롤러 이름
        
    Example:
        from app.crawlers import get_crawler
        crawler = get_crawler("music")()
        result = crawler.crawl()
    
    """
    return _crawlers.get(name)

def list_crawlers() -> Dict[str, Type[BaseCrawler]]:
    """
    등록된 모든 크롤러를 반환하는 함수
    """
    return _crawlers.copy()

# 크롤러 모듈 임포트 - 순환 참조 방지를 위해 여기서 임포트
from .music import MusicCrawler
from .news_naver import NewsNaverCrawler
from .realtime_search_words_google import RealtimeSearchWordsGoogleCrawler