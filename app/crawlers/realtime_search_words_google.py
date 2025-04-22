# 구글 실시간 검색어 크롤링 수행
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


us_realtime_url = "https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all"
kr_realtime_url = "https://trends.google.com/trends/trendingsearches/realtime?geo=KR&category=all"

def crawl_top10(country, url, limit=10):
  chrome_options = Options()
  chrome_options.add_argument("--headless")  # GUI 없이 실행
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  driver = webdriver.Chrome(options=chrome_options)

  driver.get("https://www.selenium.dev/selenium/web/web-form.html")

  driver.get(url)

  # 페이지가 로딩될 시간을 기다림
  time.sleep(2)

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

  driver.quit()
  return result

def crawl_realtime_search_words():
  crawl_urls = {
      "kr" : "https://trends.google.com/trends/trendingsearches/realtime?geo=KR&category=all",
      "us" : "https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all"
  }

  realtime_search_words = {}
  for key, url in crawl_urls.items():
    realtime_search_words[key] = crawl_top10(key, url)

  return { "realtime_search_words" : realtime_search_words }
