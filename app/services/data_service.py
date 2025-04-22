# 크롤링 수행
# 데이터를 json 형식으로 변환

# Gin에 데이터 전달
from app.crawlers.music import crawl_music
from app.crawlers.realtime_search_words_google import crawl_realtime_search_words

def music_service():
    data = crawl_music()
    return {"message": "Success", "result": data}

def realtime_search_words_service():
    data = crawl_realtime_search_words()
    return {"message": "Success", "result": data}
