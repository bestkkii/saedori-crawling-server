from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, Any
import time
from .base import BaseCrawler
from ..crawlers import register_crawler

class RealtimeSearchWordsGoogleCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.crawl_urls = {
            "kr": "https://trends.google.com/trends/trendingsearches/realtime?geo=KR&category=all",
            "us": "https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all"
        }

    def _crawl_top10(self, driver, country: str, url: str, limit: int = 10) -> list:
        """
        구글 실시간 검색어 Top 10 크롤링
        
        Args:
            driver: Selenium WebDriver
            country: 국가 코드 (kr, us)
            url: 크롤링할 URL
            limit: 가져올 검색어 수 (기본값: 10)
            
        Returns:
            list: 크롤링 결과 리스트
        """
        driver.get(url)
        time.sleep(2)  # 구글 트렌드 로딩 대기

        # 검색어 항목 찾기
        trend_elements = driver.find_elements(By.CSS_SELECTOR, "div.mZ3RIc")[:limit]
        result = []
        
        for idx, elem in enumerate(trend_elements):
            try:
                word = elem.text
                rank = str(idx + 1)
                
                result.append({
                    "country": country,
                    "search_word": word,
                    "rank": rank,
                    "timestamp": int(time.time())  # 현재 유닉스 타임스탬프
                })
            except Exception as e:
                print(f"[Error] 실시간 검색어 정보 수집 실패: {e}")
                continue
                
        return result

    def crawl(self) -> Dict[str, Any]:
        """
        모든 실시간 검색어 데이터 크롤링
        
        Returns:
            Dict[str, Any]: 크롤링 결과
            {
                "realtime_search_words": {
                    "kr": [...],
                    "us": [...]
                }
            }
        """
        driver = self._get_driver()
        
        try:
            realtime_search_words = {}
            for key, url in self.crawl_urls.items():
                realtime_search_words[key] = self._crawl_top10(driver, key, url)
                
            return {
                "realtime_search_words": realtime_search_words
            }
        except Exception as e:
            return {
                "error": str(e)
            }
        finally:
            driver.quit()

register_crawler("realtime_search_words_google", RealtimeSearchWordsGoogleCrawler)