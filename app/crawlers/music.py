from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 유튜브 뮤직 크롤링 수행

def crawl_top10(url, limit=10):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)

    time.sleep(5)

    cards = driver.find_elements(By.TAG_NAME, "ytd-playlist-video-renderer")[:limit]
    results = []

    for card in cards:
        try:
            title_element = card.find_element(By.ID, "video-title")
            title = title_element.text.strip()
            artist = card.find_element(By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.yt-formatted-string").text.strip()
            url = title_element.get_attribute("href")
            results.append({
                "singer": artist,
                "title": title,
                "url" : url
            })

        except Exception as e:
            print(f"[Error] 정보 수집 실패: {e}")
            continue

    driver.quit()
    return results


def crawl_music():
    crawl_urls = {
        "domestic" : "https://www.youtube.com/playlist?list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m",
        "global" : "https://www.youtube.com/playlist?list=PL4fGSI1pDJn6puJdseH2Rt9sMvt9E2M4i"
    }

    music_data = {}
    for key, url in crawl_urls.items():
        music_data[key] = crawl_top10(url)

    return { "music" : music_data }
