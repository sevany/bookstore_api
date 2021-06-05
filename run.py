from starlette import status
from starlette import responses
from models.book import Book
from models.author import Author
from fastapi import FastAPI, Body, Header, File
from models.user import User
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response
# from models.book import Book
# from models.author import Author

app = FastAPI()

@app.get("/hello")
async def hello_world():
    return {"hello Sevtech Users!"}


@app.get("/user")
async def validation(password:str):
    return {"query parameter": password}

@app.post("/user", status_code=HTTP_201_CREATED)
async def user(user:User, x_custom: str = Header(...)):
    return {"request body": user, "request_custom_header": x_custom}

@app.get("/book/{isbn}", response_model=Book)
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

@app.get("/author/{id}/book")
async def get_authors_book(id: int,  category: str, order: str = "asc"):
    return{"query changable parameter": order + category +str(id)}

@app.patch("/author/name")
async def patch_author_name(name:str = Body(..., embed=True)):
    return {"name in body": name}

@app.post("/user/author")
async def post_user_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user": user, "author": author, "bookstore_name": bookstore_name}



##Endpoind where user can upload their profile pictrures
@app.post("/user/photo")
async def upload_photo(response:Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    return {"file size": len(profile_photo)}