# ComicVerseAI 🚀

An automated AI comic story creator built with FastAPI, Google Gemini, and Stable Diffusion.

## 📹 Project Demo Video
[Watch the ComicVerseAI Demo Video on Google Drive](https://drive.google.com/file/d/1xMBmBokaV-_FPu1wmytjJkqGeYFUQtPQ/view?usp=drivesdk)

## 📁 Project Architecture
- `app/`: FastAPI application backend (`main.py`, `routes.py`, `gemini_flash.py`)
- `static/`: Static assets and generated comic panel images
- `templates/`: Frontend HTML interface (`index.html`)

## 🛠️ Setup & Running
1. Activate virtual environment: `.\comiccraft-env\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch server: `uvicorn app.main:app --reload`
4. Access API docs at `http://127.0.0.1:8000/docs`