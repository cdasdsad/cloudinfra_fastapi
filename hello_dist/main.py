# hello/main.py 파일

import socket
from fastapi import FastAPI

# FastAPI 객체 생성
app = FastAPI()

# 최상위 경로 요청에 대해서 응답을 처리하는 비동기 함수
@app.get("/")
async def root() :
    # dict 나 list type 을 리턴해주면 해당 객체에 담긴 정보를 json 형식의 문자열로 변환해서 fastapi 가 응답한다
    return {"message" : "Hello from fastapi"}

# 서버 상태 확인용 엔드포인트
@app.get("/health")
async def health():
    info = {"status":"ok"}
    return info

@app.get("/whoareyou")
async def who() :
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    return {"hostname": hostname, "local_ip": local_ip}