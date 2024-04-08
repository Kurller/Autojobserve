from fastapi import FastAPI
from router import scrape1

app = FastAPI()


app.include_router(scrape1.router)