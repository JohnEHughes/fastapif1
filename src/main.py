from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, sys
import database
from routers import drivers as driver_router
from routers import teams as team_router
from models import drivers
from models import teams
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

drivers.Base.metadata.create_all(bind=database.engine)
teams.Base.metadata.create_all(bind=database.engine)

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

app.include_router(driver_router.router, tags=["Drivers"], prefix="")
app.include_router(team_router.router, tags=["Teams"], prefix="")


@app.get("/")
def root():
    return {"message": "Welcome to the Formula 1 information repo"}