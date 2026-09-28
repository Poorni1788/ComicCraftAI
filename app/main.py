import os
from dotenv import load_dotenv

# Load .env file before importing routes
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(title="ComicCraft AI")

# Ensure required directories exist
os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)
os.makedirs("static/fonts", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)
