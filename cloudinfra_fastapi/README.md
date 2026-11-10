# FastAPI 기초 실습 가이드

본 문서는 FastAPI를 활용한 웹 백엔드 개발 환경 구성 및 애플리케이션 실행 방법을 안내합니다.

## 1. 개발 환경 구성

프로젝트를 시작하기 위해 독립적인 파이썬 가상 환경을 생성하고, 서버 구동에 필요한 핵심 패키지를 설치합니다. 터미널(또는 명령 프롬프트)을 열고 아래 명령어를 순서대로 실행하세요.

```bash
# 1. 파이썬 가상 환경(venv) 생성
python -m venv venv

# 2. 가상 환경 활성화 (Windows OS 기준)
.\venv\Scripts\activate

# 3. FastAPI 및 Uvicorn(비동기 웹 서버) 설치
pip install fastapi uvicorn
```

## 2. FastAPI 서버 실행

환경 구성이 완료되면 작성한 애플리케이션 코드를 실행할 수 있습니다.

```bash
# 애플리케이션 구동
uvicorn main:app --reload
```
* **`main:app`**: `main.py` 스크립트 파일 안에 정의된 `app`이라는 이름의 FastAPI 객체를 찾아 실행한다는 의미입니다.
* **`--reload`**: 소스 코드가 수정될 때마다 서버를 자동으로 재시작해 주는 매우 유용한 개발 환경용 옵션입니다.

## 3. 데이터 응답 구조 (JSON)

FastAPI는 클라이언트(웹 브라우저, 모바일 앱 등)의 요청을 처리한 뒤, 주로 **JSON (JavaScript Object Notation)** 형식의 문서로 데이터를 반환합니다. 프론트엔드는 이 JSON 데이터를 받아 화면에 적절하게 그려내는(렌더링) 역할을 수행하게 됩니다.

## 4. 대화형 API 문서 확인 (Swagger UI)

FastAPI의 가장 강력한 기능 중 하나는 API 문서를 자동으로 생성해 준다는 점입니다. 서버가 구동 중인 상태에서 웹 브라우저를 열고 아래 주소로 접속해 보세요.

* **API 테스트 문서 주소:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

이 페이지에서는 개발한 API의 목록을 한눈에 확인하고, 웹 브라우저 상에서 직접 데이터를 입력하여 테스트(Try it out)해 볼 수 있습니다.

## 5. 프로젝트 환경 복제 (의존성 관리)

현재 개발 중인 컴퓨터의 가상 환경 설정을 저장해 두면, 향후 다른 서버(AWS EC2 등)나 팀원의 PC에서도 완전히 동일한 실행 환경을 단번에 재현할 수 있습니다.

```bash
# 1. 현재 설치된 패키지 목록과 버전 정보 기록하기
pip freeze > requirements.txt

# 2. 다른 환경에서 requirements.txt를 읽어들여 동일하게 설치하기
pip install -r requirements.txt
```