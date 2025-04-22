from .headlines_naver_news import crawl_headlines_naver_news
from .realtime_search_words_google import crawl_realtime_search_words
from typing import Dict, Type
from .base import BaseCrawler

__all__ = ["crawl_headlines_naver_news", "crawl_realtime_search_words"]

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
    """등록된 크롤러를 가져오는 함수"""
    return _crawlers.get(name)
