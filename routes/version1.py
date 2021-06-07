from fastapi import FastAPI, Body, Header, File, Depends, HTTPException
from models.JWT_user import JWTUser
from starlette import status
from starlette import responses
from models.book import Book
from models.author import Author
from models.user import User
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, check_token, create_token
from models.JWT_user import JWTUser

app_v1 = FastAPI(openapi_prefix="/v1")


@app_v1.get("/hello")
async def hello_world():
    return {"hello Sevtech Users!"}


@app_v1.get("/user")
async def validation(password:str):
    return {"query parameter": password}

@app_v1.post("/user", status_code=HTTP_201_CREATED)
async def user(user:User, x_custom:str = Header("default")):
    return {"request body": user, "request_custom_header": x_custom}

@app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"])
async def get_book(isbn:str):
    author_dict ={
        "name": "author1",
        "book": ["book1", "book2"]
    }
    author1 = Author(**author_dict)
    book_dict ={
        "isbn": "isbn1",
        "name": "book1",
        "author": author1,
        "year": 2009
    }

    book1 = Book(**book_dict)
    return book1

@app_v1.get("/author/{id}/book")
async def get_authors_book(id: int,  category: str, order: str = "asc"):
    return{"query changable parameter": order + category +str(id)}

@app_v1.patch("/author/name")
async def patch_author_name(name:str = Body(..., embed=True)):
    return {"name in body": name}

@app_v1.post("/user/author")
async def post_user_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user": user, "author": author, "bookstore_name": bookstore_name}



##Endpoind where user can upload their profile pictrures
@app_v1.post("/user/photo")
async def upload_photo(response:Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    return {"file size": len(profile_photo)}

##endpoint generate token for users

@app_v1.post("/token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#check if nama correct ke tak

    jwt_user_dict = {
        "username": form_data.username,
        "password": form_data.password
    }
    
    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)
    
#kalau fail takde nama and pasword kat db kena return unathourized status
    if user is None:
        # return HTTP_401_UNAUTHORIZED
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED) #if nak guna http exception
#kalau ada dalam db boleh create token
    jwt_token = create_token(user)
    return{"token": jwt_token}
