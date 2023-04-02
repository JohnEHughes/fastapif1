from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import engine
from routers import drivers
from models import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API F1",
    description="Formula 1 information repository",
    version="0.0.1",
    contact={
        "name": "John Hughes",
        "email": "john.hughes@arcticshores.com"
    }
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drivers.router, tags=["Drivers"], prefix="")


@app.get("/healthchecker")
def root():
    return {"message": "Welcome to the Formula 1 information repo"}