
from fastapi import FastAPI, Body, Header, File
from starlette import middleware, responses
from starlette.status import HTTP_401_UNAUTHORIZED
from routes.version1 import app_v1
# from passlib.context import CryptContext
from starlette.requests import Request
from utils.security import check_token
from starlette.responses import Response
from datetime import datetime


app = FastAPI()

##mount version one 
app.mount("/v1", app_v1)


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    #nak try check JWT token in coming requests 
    if not str(request.url).__contains__("/token"):
        try:

            jwt_token = request.headers["Authorization"].split("Bearer ")[1]
            valid = check_token(jwt_token)
        except Exception as e:
            valid = False

        if not valid :
            return Response("Unathorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)
    execution_time  = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response
