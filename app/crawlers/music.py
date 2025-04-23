from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Init driver
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Crawling melon
def crawl_melon(driver, url):
    driver.get(url)

    time.sleep(5)

    results = []

    for idx in range(1, 11):
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
                "singer" : singer,
                "url": "https://www.melon.com/album/detail.htm?albumId=" + album_id
            })

        except Exception as e:
            print(f"[Error] 곡 처리 실패: {e}")
            continue

    return results


# Crawling spotify
def crawl_spotify(driver, url):
    driver.get(url)

    time.sleep(5)

    results = []
    
    for idx in range (1, 11):
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
                "singer" : singer,
                "url": url_src
            })

        except Exception as e:
            print(f"[Error] 곡 처리 실패: {e}")
            continue

    return results


def crawl_music():
    
    driver = create_driver()

    music_data = {}
    music_data["melon"] = crawl_melon(driver, "https://www.melon.com/chart/index.htm",)
    music_data["spotify"] = crawl_spotify(driver, "https://charts.spotify.com/home",)
    
    driver.quit()

    return { "music" : music_data }
