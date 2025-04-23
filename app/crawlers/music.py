from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, Any
import time
import re
from .base import BaseCrawler
from ..crawlers import register_crawler

class MusicCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.crawl_urls = {
            "melon": "https://www.melon.com/chart/index.htm",
            "spotify": "https://charts.spotify.com/home"
        }

    def _crawl_melon(self, driver, url: str, limit: int = 10) -> list:
        """
        멜론 Top 10 크롤링
        
        Args:
            driver: Selenium WebDriver
            url: 크롤링할 URL
            limit: 가져올 곡 수 (기본값: 10)
            
        Returns:
            list: 크롤링 결과 리스트
        """
        driver.get(url)
        time.sleep(5)  # 멜론 차트 로딩 대기

        results = []
        for idx in range(1, limit + 1):
            try:
                # 제목 추출
                title_tag = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div/div/div[3]/form/div/table/tbody/tr[{idx}]/td[6]/div/div/div[1]/span/a')
                title = title_tag.text.strip()
                
                # 가수 추출
                singer_tag = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div/div/div[3]/form/div/table/tbody/tr[{idx}]/td[6]/div/div/div[2]/a')
                singer = singer_tag.text.strip()
                
                # URL 추출
                url_tag = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div/div/div[3]/form/div/table/tbody/tr[{idx}]/td[4]/div/a')
                url_src = url_tag.get_attribute('href')
                album_id = re.search(r"goAlbumDetail\('(\d+)'\)", url_src).group(1)
                
                results.append({
                    "title": title,
                    "singer": singer,
                    "url": f"https://www.melon.com/album/detail.htm?albumId={album_id}"
                })
            except Exception as e:
                print(f"[Error] 곡 처리 실패: {e}")
                continue
                
        return results

    def _crawl_spotify(self, driver, url: str, limit: int = 10) -> list:
        """
        스포티파이 Top 10 크롤링
        
        Args:
            driver: Selenium WebDriver
            url: 크롤링할 URL
            limit: 가져올 곡 수 (기본값: 10)
            
        Returns:
            list: 크롤링 결과 리스트
        """
        driver.get(url)
        time.sleep(5)  # 스포티파이 차트 로딩 대기

        results = []
        for idx in range(1, limit + 1):
            try:
                # 제목 추출
                title_xpath = f'/html/body/div/div/div/section[4]/div/ol/div[{idx}]/li/div[3]/p'
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, title_xpath)))
                title_tag = driver.find_element(By.XPATH, title_xpath)
                title = title_tag.get_attribute('innerText').strip()
                
                # 가수 추출
                singer_xpath = f'/html/body/div/div/div/section[4]/div/ol/div[{idx}]/li/div[3]//span[@data-testid="artists-names"]/a'
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, singer_xpath)))
                singer_tags = driver.find_elements(By.XPATH, singer_xpath)
                singers = [a.get_attribute('innerText').strip() for a in singer_tags]
                singer = ", ".join(singers)

                # URL 추출
                url_tag = driver.find_element(By.XPATH, f'/html/body/div/div/div/section[4]/div/ol/div[{idx}]/li/div[1]/a')
                url_src = url_tag.get_attribute('href')
                
                results.append({
                    "title": title,
                    "singer": singer,
                    "url": url_src
                })
            except Exception as e:
                print(f"[Error] 곡 처리 실패: {e}")
                continue
                
        return results

    def crawl(self) -> Dict[str, Any]:
        """
        모든 뮤직 데이터 크롤링
        
        Returns:
            Dict[str, Any]: 크롤링 결과
            {
                "music": {
                    "melon": [...],
                    "spotify": [...]
                }
            }
        """
        driver = self._get_driver()
        
        try:
            music_data = {}
            music_data["melon"] = self._crawl_melon(driver, self.crawl_urls["melon"])
            music_data["spotify"] = self._crawl_spotify(driver, self.crawl_urls["spotify"])
                
            return {
                "crawling": "Success",
                "result": {"music": music_data}
            }
        except Exception as e:
            return {
                "crawling": "Failed",
                "result": {"error": str(e)}
            }
        finally:
            driver.quit()

register_crawler("music", MusicCrawler)