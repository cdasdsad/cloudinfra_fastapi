from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
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


@app.get("/member", response_class=HTMLResponse)
def getMembers(req: Request, db: Session = Depends(get_db)):
    query = text("""
        SELECT num, name, addr
        FROM post
        ORDER BY num ASC
    """)

    # db 객체를 이용해서 회원 목록 얻어오기
    result = db.execute(query)

    # 회원 목록이 들어있는 list type 이라고 생각하면 된다
    members = result.fetchall()
    # 응답하기
    return templates.TemplateResponse(
        request=req, name="member/list.html", context={"members": members}
    )


@app.get("/member/new", response_class=HTMLResponse)
def memberNewForm(req: Request):
    return templates.TemplateResponse(request=req, name="member/new.html")


@app.post("/member/new", response_class=HTMLResponse)
def memberNew(
    req: Request,
    name: str = Form(...),
    addr: str = Form(...),
    db: Session = Depends(get_db),
):
    query = text("""
        INSERT INTO post
        (name, addr)
        VALUES(:name , :addr);
    """)
    # query 문을 실행하면서 같이 전달한 dict 의 키값과 :name , :addr 동일한 위치에 값이 바인딩 되어서 실행한다.
    db.execute(query, {"name": name, "addr": addr})
    # insert, update, delete 문은 commit() 을 호출해야 실제로 DB 에 반영된다.
    db.commit()
    # 응답하기
    return templates.TemplateResponse(
        request=req,
        name="member/alert.html",
        context={"msg": f"{name} 님의 정보를 저장했습니다", "url": "/member"},
    )


# {num} <- 전달되는 마지막 경로의 값을 num이라는 변수에 담겠다는 의미
@app.get("/member/delete/{num}", response_class=HTMLResponse)
def deleteMember(num: int, db: Session = Depends(get_db)):
    query = text("""
        DELETE FROM post
        WHERE num = :num
    """)
    # 삭제할 회원의 번호를 dict에 "num" 이라는 키값으로 전달하면 :num 위치에 바인딩 되어서 실행된다.
    db.execute(query, {"num": num})
    # commit() 을 호출해야 실제 반영됨
    db.commit()
    # 응답하기
    # 리다이렉트 응답은 웹브라우저에게 새로운 경로로 다시 요청을 하라고 강요하는 응답이다
    # 웹브라우저는 말을 잘 듣기 때문에 강요하는대로 "/member" 경로로 요청을 다시한다
    # 결과적으로 삭제후에 /member 페이지를 새로고침 하는 효과가 된다.
    return RedirectResponse("/member", status_code=302)


@app.get("/member/edit/{num}")
def memberEditForm(req: Request, num: int, db: Session = Depends(get_db)):
    # 수정할 회원의 정보를 읽어오기 위한 query
    query = text("""
        SELECT num,name,addr
        FROM post
        WHERE num =:num
    """)
    # select 되는 row 가 최대 1개 이기 때문에 .fetchall() 이 아닌 .fetchone() 을 호출한다
    # 리턴되는 것은 dict 라고 생각하고 생각하면 된다.
    row = db.execute(query, {"num": num}).fetchone()
    # 수정폼을 응답한다
    return templates.TemplateResponse(
        request=req, name="member/edit.html", context={"row": row}
    )


@app.post("/member/update")
def memberUpdate(
    req: Request,
    num: int = Form(...),
    name: str = Form(...),
    addr: str = Form(...),
    db: Session = Depends(get_db),
):
    query = text("""
        UPDATE post
        SET name = :name, addr = :addr
        WHERE num = :num
    """)
    db.execute(query, {"num": num, "name": name, "addr": addr})
    db.commit()
    return templates.TemplateResponse(
        request=req,
        name="member/alert.html",
        context={"msg": f"{name} 님의 정보를 수정했습니다", "url": "/member"},
    )
