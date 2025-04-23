# saedori-crwaling-server
---
- FastAPI 서버입니다.


## 디렉터리 구조
---
    app/
    ├── api/
    │   └── v1/
    │       ├── endpoints/
    │       │   └── crawling.py
    │       ├── __init__.py
    │       └── router.py
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    ├── crawlers/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── music.py
    │   ├── music_prev.py
    │   ├── news_naver.py
    │   ├── realtime_search_words_google.py
    │   └── realtime_search_words_google_prev.py
    ├── logs/
    ├── services/
    │   ├── __init__.py
    │   ├── data_service.py
    │   └── data_service_multiprocessing.py
    ├── __pycache__/
    ├── main.py
    ├── testtttt.py
    └── utils.py

---
---
<br><br><br><br>
## 코드 리뷰 보고서
---
#### Saedori Crawling Server 코드 리뷰 보고서

##### 1. 프로젝트 개요
###### &emsp;  Saedori Crawling Server는 Gin 서버로부터 크롤링 요청을 받아 여러 웹사이트의 데이터를 수집하고 결과를 반환하는 FastAPI 기반 서버입니다. 멀티프로세싱을 활용하여 여러 크롤링 작업을 병렬로 처리합니다.

##### 2. 폴더 구조 및 근거
    app/
    ├── api/ # API 엔드포인트 정의 (v1 버전 관리)
    ├── crawlers/ # 각 웹사이트별 크롤러 구현
    ├── services/ # 비즈니스 로직 및 크롤링 작업 관리
    ├── config/ # 설정 파일 관리
    ├── logs/ # 로그 파일 저장
    └── main.py # 애플리케이션 진입점
###### &emsp;  폴더 구조는 관심사 분리 원칙에 따라 API, 크롤러, 서비스 계층으로 명확히 구분하여 코드의 유지보수성과 확장성을 높였습니다.

##### 3. 주요 파일 및 기능

###### 3.1 main.py
###### &emsp;  FastAPI 애플리케이션 설정, CORS 미들웨어 구성, API 라우터 등록을 담당합니다.

###### 3.2 api/v1/endpoints/crawling.py
###### &emsp;  Gin 서버로부터 `/api/v1/crawl` 경로로 들어오는 GET 요청을 처리하고 크롤링 결과를 반환합니다.

###### 3.3 api/v1/router.py
###### &emsp;  API 버전 관리 및 엔드포인트 라우팅을 담당합니다.

###### 3.4 services/data_service.py
###### &emsp;  크롤링 작업의 조율과 결과 관리를 담당하며, 멀티프로세싱을 통해 여러 크롤러를 병렬로 실행합니다.

###### 3.5 crawlers/base.py
###### &emsp;  모든 크롤러의 기본 클래스로, Selenium WebDriver 설정 및 공통 기능을 제공합니다.

###### 3.6 crawlers/music.py, news_naver.py, realtime_search_words_google.py
###### &emsp;  각 웹사이트별 크롤링 로직을 구현한 클래스들입니다.

##### 4. 데이터 흐름 및 기능 구현

###### 4.1 Gin에서 크롤링 요청 받기
###### &emsp; 1. Gin 서버가 `/api/v1/crawl` 경로로 GET 요청을 보냅니다.
###### &emsp; 2. FastAPI의 라우터가 요청을 받아 `crawling.py`의 `crawl()` 함수를 호출합니다.
###### &emsp; 3. `crawl()` 함수는 `data_service.crawl_all()`을 호출하여 크롤링 작업을 시작합니다.

###### 4.2 멀티프로세싱을 통한 크롤링 작업 실행
###### &emsp; 1. `data_service.py`의 `crawl_all()` 메서드에서 `ProcessPoolExecutor`를 사용하여 멀티프로세싱을 구현합니다.
###### &emsp; 2. 각 크롤러는 별도의 프로세스에서 실행되어 병렬로 데이터를 수집합니다.
###### &emsp; 3. `_run_crawler()` 메서드는 각 크롤러의 `crawl()` 메서드를 호출하고 결과를 반환합니다.

###### 4.3 크롤링 수행
###### &emsp; 1. 각 크롤러 클래스는 `BaseCrawler`를 상속받아 `crawl()` 메서드를 구현합니다.
###### &emsp; 2. `_get_driver()` 메서드는 환경(GCP/로컬)에 따라 적절한 ChromeDriver를 설정합니다.
###### &emsp; 3. 크롤러는 Selenium을 사용하여 웹페이지에서 데이터를 추출합니다.

###### 4.4 Gin에게 데이터 전달
###### &emsp; 1. 모든 크롤링 작업이 완료되면 결과가 수집되어 `crawl_all()` 메서드에서 반환됩니다.
###### &emsp; 2. `crawl()` 함수는 결과를 검증하고 Gin 서버에 응답합니다.
###### &emsp; 3. 응답은 JSON 형식으로 반환되며, 각 크롤러의 결과가 포함됩니다.

##### 5. 핵심 기술 및 구현 방식

###### 5.1 멀티프로세싱
###### &emsp; - `concurrent.futures.ProcessPoolExecutor`를 사용하여 크롤링 작업을 병렬로 실행합니다.
###### &emsp; - 각 크롤러는 독립적인 프로세스에서 실행되어 서로 영향을 주지 않습니다.
###### &emsp; - 타임아웃 설정을 통해 무한 대기 상태를 방지합니다.

###### 5.2 Selenium WebDriver
###### &emsp; - `BaseCrawler` 클래스에서 ChromeDriver 설정을 관리합니다.
###### &emsp; - 환경(GCP/로컬)에 따라 자동으로 적절한 ChromeDriver를 선택합니다.
###### &emsp; - 메모리 최적화 옵션을 적용하여 리소스 사용을 최소화합니다.

###### 5.3 에러 처리 및 로깅
###### &emsp; - 각 크롤러의 에러를 독립적으로 처리하여 한 크롤러의 실패가 전체 작업에 영향을 주지 않도록 합니다.
###### &emsp; - 로깅 시스템을 통해 크롤링 과정과 에러를 추적합니다.

##### 6. 개선 가능한 부분

###### &emsp; 1. **캐싱 메커니즘**: 자주 요청되는 데이터에 대한 캐싱을 구현하여 성능을 향상시킬 수 있습니다.
###### &emsp; 2. **재시도 메커니즘**: 일시적인 네트워크 문제 등으로 인한 크롤링 실패에 대한 재시도 로직을 추가할 수 있습니다.
###### &emsp; 3. **모니터링 시스템**: 크롤링 작업의 상태와 성능을 모니터링하는 시스템을 구축할 수 있습니다.
###### &emsp; 4. **테스트 코드**: 단위 테스트와 통합 테스트를 추가하여 코드의 안정성을 높일 수 있습니다.

##### 7. 결론
###### Saedori Crawling Server는 FastAPI와 Selenium을 활용하여 효율적인 웹 크롤링 시스템을 구현했습니다. 멀티프로세싱을 통해 여러 크롤링 작업을 병렬로 처리하며, 환경에 따라 자동으로 적절한 설정을 적용합니다. 이 구조는 확장성이 높고 유지보수가 용이하며, Gin 서버와의 통합이 원활합니다.