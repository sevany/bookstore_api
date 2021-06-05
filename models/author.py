# from models.book import Book
from typing import List
from pydantic import BaseModel
# import enum
# from fastapi import Query
# from models.book import Book
from typing import List

class Author(BaseModel):
    name: str
    book: List[str]