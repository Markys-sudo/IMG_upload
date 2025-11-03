# app.py
import os
import uuid
import logging
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse

# Конфігурація шляхів
IMAGES_DIR = "/images"
LOGS_DIR = "/logs"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 МБ
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}

# Переконаємось, що папки існують
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Налаштування логування
log_file = os.path.join(LOGS_DIR, "app.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI(title="Image Hosting Service")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Image Hosting Service</title>
        </head>
        <body>
            <h1>Ласкаво просимо до Image Hosting Service!</h1>
            <p>Ви можете завантажувати зображення та отримувати прямі посилання.</p>
            <ul>
                <li><a href="/upload_form">Завантажити зображення</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/upload_form", response_class=HTMLResponse)
async def upload_form():
    return """
    <html>
        <head>
            <title>Завантажити зображення</title>
        </head>
        <body>
            <h2>Завантажити зображення</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept=".jpg,.jpeg,.png,.gif">
                <input type="submit" value="Завантажити">
            </form>
        </body>
    </html>
    """

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()

    # Перевірка формату файлу
    if extension not in ALLOWED_EXTENSIONS:
        msg = f"Непідтримуваний формат файлу ({filename})"
        logging.error(msg)
        raise HTTPException(status_code=400, detail=msg)

    # Перевірка розміру файлу
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        msg = f"Файл перевищує 5 МБ ({filename})"
        logging.error(msg)
        raise HTTPException(status_code=400, detail=msg)

    # Генерація унікального імені
    unique_name = f"{uuid.uuid4().hex}{extension}"
    save_path = os.path.join(IMAGES_DIR, unique_name)

    # Збереження файлу
    with open(save_path, "wb") as f:
        f.write(contents)

    logging.info(f"Успіх: зображення {unique_name} завантажено.")

    return {
        "filename": unique_name,
        "url": f"/images/{unique_name}"
    }
