from typing import Optional
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Book
#from app.settings import DATABASE_URL

DATABASE_URL = "postgresql://postgres:root@localhost/fastapi"

##req-res pydentic model
class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


recreate_database()

##SWAGGER UI CONFIGURATIONS
app = FastAPI(swagger_ui_parameters={   
                                        "displayOperationId": "false",
                                        "defaultModelsExpandDepth" : 1,
                                        "displayRequestDuration": "false",
                                        "docExpansion": "list",
                                        "tryItOutEnabled": "false"
                                    })

@app.get("/")
def root():
    return {"message": "A simple CRUD API created with FastAPI and SQLAlchemy for PostgreSQL, is UP and RUNNING"}


##CREATING A BOOK
@app.post("/books")
def create_book(title: str, author: str, content: str):
    session = Session()
    book = Book(title=title, author=author, content=content)
    session.add(book)
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )


##GET A BOOK BY ID
@app.get("/books/{id}")
def find_book(id: int):
    session = Session()
    book = session.query(Book).filter(Book.id == id).first()
    session.close()

    result = jsonable_encoder({"book": book})

    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


##GET ALL THE BOOKS
@app.get("/books")
def get_books():
    session = Session()
    books = session.query(Book).all()
    session.close()

    result = jsonable_encoder({"books": books})

    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


##UPDATE A BOOK BY ID
@app.put("/books/{id}")
def update_book(id: int, bookModel: BookUpdateModel):
    session = Session()
    book = session.query(Book).get(id)

    if book is None:
        return JSONResponse(
            status_code=400, content={"status_code": 400, "message": "Book not Found"}
        )

    if bookModel.title is not None:
        book.title = bookModel.title
    if bookModel.author is not None:
        book.author = bookModel.author
    if bookModel.content is not None:
        book.content = bookModel.content    
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )


##DELETING A BOOK BY ID
@app.delete("/books/{id}")
def delete_book(id: int):
    session = Session()
    book = session.query(Book).get(id)

    if book is None:
        return JSONResponse(
            status_code=400, content={"status_code": 400, "message": "Book not Found"}
        )

    session.delete(book)
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )
