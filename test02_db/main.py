from fastapi import Depends, FastAPI, Form, Request
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

@app.get("/member/new", response_class = HTMLResponse)
def memberNewForm(req : Request) :
    return templates.TemplateResponse(
        request= req,
        name = "member/new.html"
    )

@app.post("/member/new", response_class=HTMLResponse)
def memberNew(req: Request, name :str = Form(...), addr: str = Form(...), db : Session = Depends(get_db)):
    query = text("""
        INSERT INTO post
        (name, addr)
        VALUES(:name , :addr);
    """)
    # query 문을 실행하면서 같이 전달한 dict 의 키값과 :name , :addr 동일한 위치에 값이 바인딩 되어서 실행한다.
    db.execute(query, {"name" : name ,"addr" : addr})
    # insert, update, delete 문은 commit() 을 호출해야 실제로 DB 에 반영된다.
    db.commit()
    # 응답하기
    return templates.TemplateResponse(
        request = req,
        name = "member/alert.html",
        context= {
            "msg":f"{name} 님의 정보를 저장했습니다",
            "url" : "/member"
        }
    )