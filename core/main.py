from fastapi import FastAPI
from core.routes import authors, books, users, auth, operations


app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(operations.router)
