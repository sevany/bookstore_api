from logging import INFO
from passlib.context import CryptContext
from typing import final

from starlette.status import HTTP_401_UNAUTHORIZED
from models.JWT_user import JWTUser

from datetime import datetime, timedelta
from utils.pass_authen import JWT_EXPIRATION_TIMES_MINUTES, JWT_ALGORITH, JWT_SECRET_KEY
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

import jwt
import time
# #password best if it comes with hash
# wen need to encrypt password when we storing them in db
##FIRST THINGS
####################################################################################
password_con = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


jwt_usertest = {"username": "testing", 
                "password":"$2b$12$bL6jVcVY7svupKgL0rSzxummjFIaUrPDYPZYs25oPrXqzfVQJ23jW",
                "disbled":False, 
                "role":"admin"}

fake_usertest = JWTUser(**jwt_usertest)
# jwt_fake_db = [{}]


def get_hashed_password(passwordnye):
    return password_con.hash(passwordnye)

##ni nak make sure password original sama tak dgn hash password
def verify_password(plain_password, hashed_password):
    try:
        return password_con.verify(plain_password, hashed_password)
    except Exception as e:
        return "AHHH COBA LAGI!"


# print(get_hashed_password("aposajo"))
# hashed = "$2b$12$pncsZ4BhvNUgbVGNLCPGXu8xw/2w2tbidOrx64WZwzvnj0gzJNDvG"

# print(verify_password("mysecret", hashed))

############################################################################################

#SECOND THINGS
#########################################################################################

##authenticate username and password to pass JWT to users token

# this function means user send username ands pass in form URL form requests untuk dpt token
#check if we have such user in db or not
 
def authenticate_user(user:JWTUser):
    if fake_usertest.username == user.username:
        if verify_password(user.password, fake_usertest.password):
            user.role = "admin"
            return user
    return None
# with this, everytime user nk requests api, we can authenticate if the given pass/username are corrct or not



#create access JWT token
def create_token(user:JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIMES_MINUTES)
    payload = {"sub": user.username,
               "role": user.role,
               "exp": expiration}

    jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITH)
    return jwt_token



#check whether JWT token is correct

def check_token(token:str =Depends(oauth_schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITH)
        username = payload.get("sub")
        role = payload.get("role")
        #check if we have this unique name in db or not
        expiration = payload.get("exp")
        if time.time() < expiration:
            if fake_usertest.username == username:
                return last_checks(role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
        # return False

    # raise False
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

def last_checks(role:str):
    if role == "admin":
        return True

    else: 
        # return False
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

# # print(get_hashed_password("aposajo"))
