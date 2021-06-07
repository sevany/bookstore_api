
from fastapi import FastAPI, Body, Header, File
from routes.version1 import app_v1
from passlib.context import CryptContext

app = FastAPI()

##mount version one 
app.mount("/v1", app_v1)
