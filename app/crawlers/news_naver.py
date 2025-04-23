from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Dict, Any, List
from .base import BaseCrawler
from ..crawlers import register_crawler

class NewsNaverCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.crawl_urls = {
            "news_naver": "https://news.naver.com/main/ranking/popularDay.naver",
        }

    def _crawl_news(self, driver: webdriver.Chrome, url: str) -> List[Dict[str, str]]:
        """
        언론사 별 1위 랭킹뉴스 5개 크롤링 수행

        Args:
            driver: Selenium WebDriver
            url: 크롤링할 URL

        Returns:
            List[Dict[str, Any]]: 크롤링 결과
            [
                {
                    "company": "뉴시스",
                    "title": "6일 황금연휴의 꿈 사라진다…정부 "5월2일 임시공휴일 검토 안해"",
                    "lead": None,
                    "url": "https://n.news.naver.com/article/003/0013201902?ntype=RANKING",
                },
                ...
            ]
        """
        driver.get(url)
        
        # 페이지 로딩 대기
        WebDriverWait(driver, self.timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # 랭킹 뉴스 컨테이너 대기
        WebDriverWait(driver, self.timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_officeCard0"))
        )
        
        # 랭킹 뉴스 박스들 추출
        news_items = []
        ranking_boxes = driver.find_elements(By.CLASS_NAME, "rankingnews_box")[:5]  # 상위 5개만 추출
        
        for box in ranking_boxes:
            try:
                # 언론사명 추출
                company = box.find_element(By.CLASS_NAME, "rankingnews_name").text
                
                # 첫 번째 뉴스 항목의 제목과 URL 추출
                first_news = box.find_element(By.CSS_SELECTOR, "ul.rankingnews_list > li:first-child")
                title = first_news.find_element(By.CLASS_NAME, "list_title").text
                url = first_news.find_element(By.CLASS_NAME, "list_title").get_attribute("href")
                
                news_items.append({
                    "company": company,
                    "title": title,
                    "lead": None,
                    "url": url
                })
            except (NoSuchElementException, TimeoutException) as e:
                continue
                
        return news_items

    def crawl(self) -> Dict[str, Any]:
        """
        네이버 뉴스 인기 검색어를 크롤링하고 결과를 반환하는 메서드
        """
        driver = self._get_driver()
        
        try:
            news_data = []
            for url in self.crawl_urls.values():
                news_data.extend(self._crawl_news(driver, url))
                
            return {
                "crawling": "Success",
                "result": {"news": news_data}
            }
        except Exception as e:
            return {
                "crawling": "Failed",
                "result": {"error": str(e)}
            }
        finally:
            driver.quit()

# 크롤러 등록
register_crawler("news_naver", NewsNaverCrawler)