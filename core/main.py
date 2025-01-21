from fastapi import FastAPI
from core.routes import authors, books, users, auth


app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)
app.include_router(auth.router)
