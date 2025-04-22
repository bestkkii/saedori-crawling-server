# 크롤링 결과 DB에 저장

# Gin에 데이터 전달
from app.crawlers.music import crawl_music

def music_service():
    data = crawl_music()
    return {"message": "Success", "result": data}

