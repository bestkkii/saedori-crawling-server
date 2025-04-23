from crawlers import get_crawler, list_crawlers

# 등록된 크롤러 목록 출력
print("등록된 크롤러:", list_crawlers().keys())

# 특정 크롤러 가져오기
music_crawler = get_crawler("music")
if music_crawler:
    print("Music 크롤러가 등록되어 있습니다.")
else:
    print("Music 크롤러가 등록되어 있지 않습니다.")