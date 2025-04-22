# saedori-crwaling-server
---
- FastAPI 서버입니다.


## 디럭터리 구조
---
    app/
    ├── main.py                              # 메인 실행 파일
    ├── api/                                 # 요청/응답 처리
    │   └── v1/
    │       ├── __init__.py
    │       └── routes.py
    ├── crawlers/                            # 크롤링 구현
    │   ├── __init__.py
    │   ├── base.py                          # 크롤러 부모 클래스
    │   ├── headlines_naver_news.py          # 기사
    │   ├── realtime_search_words_google.py  # 실시간 검색어
    │   ├── realtime_search_words_naver.py   # (deprecated) 실시간 검색어
    │   ├── upbit.py                         # 코인
    │   └── youtube_music.py                 # 노래
    ├── services/                            # 크롤링 수행, 데이터 가공
    │   ├── __init__.py
    │   └── data_service.py
    ├── config/                              # 환경 설정
    │   ├── __init__.py
    │   └── settings.py
    ├── logs/                                # 로그 (필요하면 사용)
    ├── utils.py
    └── requirements.txt


## 실행 방법
---
1. 패키지 설치 : pip install fastapi "uvicorn[standard]"
