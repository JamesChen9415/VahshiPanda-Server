from fastapi import Depends, FastAPI

# from .dependencies import get_query_token, get_token_header

import asyncio

# from .internal import admin
from routers import users, chat

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()


app.include_router(users.router)
app.include_router(chat.router)
# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.on_event("startup")
async def startup():
    return "Starting up..."


@app.get("/")
async def root():
    print("------- test root --------")
    return {"message": "Hello Bigger Applications!"}


@app.api_route("/api/v1/greet/{id}", methods=["GET"])
async def greet(id: int):
    print(f"Received a http request, {id}")

    await asyncio.sleep(1)  # simulate backend process which take 1 seconds

    return f"Helloworld, {id}", 200
