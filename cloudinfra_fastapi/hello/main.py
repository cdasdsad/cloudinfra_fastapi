# hello/main.py 파일

import socket

from fastapi import FastAPI

# FastAPI 객체 생성
app = FastAPI()

# GET 방식 최상위 경로 요청에 대해서 응답을 처리하는 비동기 함수 
@app.get("/")
async def root():
    # dict 나 list type 을 리턴해주면 해당 객체에 담긴 정보를 json 형식의 문자열로 변환해서 fastapi 가 응답한다 
    return {"message":"Hello from fastapi"}

@app.get("/health")
async def health():
    info = {"status":"ok"}
    return info

@app.get("/whoareyou")
async def who():
    # 서버의 host 이름 가져오기 
    hostname=socket.gethostname()
    # hostname 을 이용해서 서버의 ip 주소 알아내기
    local_ip=socket.gethostbyname(hostname)
    # dict 에 응답할 정보를 담고 
    info={
        "hostname":hostname,
        "local_ip":local_ip
    }
    # dict 를 리턴하면 json 문자열로 변환 되어서 응답된다
    return info