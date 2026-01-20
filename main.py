from fastapi import FastAPI, Request, HTTPException
from app.exceptions import EmailNotAllowedNameExistsError, UserNotFoundError
from app.api.route.user_routers import router as user_router
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI()


# 임시 데이터 저장소 (DB 대신)
todos = []

class Todo(BaseModel):
    id: Optional[int] = None
    content: str
    created_at: Optional[datetime] = None

@app.post("/todos")
async def create_todo(todo: Todo):
    todo.id = len(todos) + 1
    todo.created_at = datetime.now()
    todos.append(todo)
    return todo

@app.get("/todos")
async def get_todos():
    return todos

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    global todos
    todos = [t for t in todos if t.id != todo_id]
    return {"message": "success"}


@app.exception_handler(EmailNotAllowedNameExistsError)
async def email_not_allowed_handler(request: Request, exc: EmailNotAllowedNameExistsError):
    return JSONResponse(
        status_code=409,
        content={"error": "Email Not Allowed", "message": str(exc)}#릴리즈요?
    )


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "User Not Found", "message": str(exc)}
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": "Bad Request", "message": str(exc)}
    )
#야아아아아아호

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP Exception", "message": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": "Something went wrong"}
    )



app.include_router(user_router)


@app.get("/hello")
def hello():
    return {"message": "Hello FastAPI!"}
