from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# 테스트로 get_db 를 import 해보자
result = get_db


@app.get("/", response_class=HTMLResponse)
def index(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="index.html",
        context={
            "noticeList": ["오후 일정이 시작되었습니다", "어쩌구...", "저쩌구..."]
        },
    )


@app.get("/member", response_class =HTMLResponse)
def getMembers(req: Request, db : Session = Depends(get_db)) :
    query = text("""
        SELECT num, name, addr
        FROM post
        ORDER BY num ASC
    """)

    # db 객체를 이용해서 회원 목록 얻어오기
    result = db.execute(query)

    # 회원 목록이 들어있는 list type 이라고 생각하면 된다
    members = result.fetchall()
    #응답하기
    return templates.TemplateResponse(
        request= req,
        name = "member/list.html",
        context = {
            "members" : members
            }
    )