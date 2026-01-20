1. Python & FastAPI 버그 수정 (정답 코드)가장 많이 고쳤던 main.py와 exceptions.py의 핵심 내용입니다.main.py (임포트 및 핸들러 추가)파이썬이 인식하지 못했던 클래스들을 상단에 정의해 주었습니다.Pythonfrom fastapi import FastAPI, Request, HTTPException  # Request, HTTPException 추가
from app.exceptions import EmailNotAllowedNameExistsError, UserNotFoundError # 커스텀 에러 추가

@app.exception_handler(EmailNotAllowedNameExistsError)
async def email_not_allowed_handler(request: Request, exc: EmailNotAllowedNameExistsError):
    # 에러 발생 시 처리 로직
    ...
app/exceptions.py (파일 신규 생성)존재하지 않았던 커스텀 예외 클래스들을 직접 만들어 주었습니다.Pythonclass EmailNotAllowedNameExistsError(Exception):
    def __init__(self, message="Email not allowed or Name already exists"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)
2. Docker & 서버 실행 명령어실제 서버를 가동하기 위해 사용한 명령어입니다.DB 실행: sudo docker run을 통해 MySQL을 띄웠습니다.서버 실행 (Uvicorn):Bash# 환경변수와 함께 실행 (포트 8000A 오타 주의!)
DB_HOST=localhost DB_USER=root DB_PASSWORD=password DB_NAME=upstage \
uv run uvicorn main:app --host 0.0.0.0 --port 8000
3. Git 동기화 명령어 (가장 중요한 흐름)서버의 정답을 GitHub을 거쳐 로컬로 가져온 과정입니다.EC2 서버에서 (Push)Bashgit add .
git commit -m "fix: all bugs on ec2 server"
git push origin main --force  # 내 리포지토리로 강제 업데이트
로컬 PC에서 (Pull & Sync)내 리포지토리(network)의 내용을 로컬 브랜치들에 반영했습니다.Bash# 1. 내 리포지토리 정보 가져오기
git fetch network

# 2. 각 브랜치를 서버 정답과 일치시키기
git checkout release/0.0.1
git reset --hard network/main

git checkout main
git reset --hard network/main
4. 에러 해결 팁 요약오늘 우리가 해결한 에러 메시지들의 의미입니다.에러 메시지원인해결책NameError변수나 클래스가 정의되지 않음import 문 추가ImportError파일은 있는데 함수가 없음해당 파일에 함수(def) 추가non-fast-forward서버와 로컬의 코드가 꼬임git push --force 사용Invalid value for --port포트 번호에 숫자가 아닌 문자 포함8000A -> 8000 수정