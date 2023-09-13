from fastapi import FastAPI, Response
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/.well-known/acme-challenge/{challenge_route}")
async def get_certificate():
    return "success"
