from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uvicorn

app = FastAPI()

# === Шляхи ===
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = BASE_DIR / "images"

IMAGES_DIR.mkdir(exist_ok=True)

# === Статичні файли ===
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")


# === Головна сторінка ===
@app.get("/", response_class=HTMLResponse)
async def index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return HTMLResponse("<h1>Static index.html not found</h1>", status_code=404)


# === Завантаження файлу ===
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = IMAGES_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse({
            "filename": file.filename,
            "url": f"http://localhost:8080/images/{file.filename}"
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# === Повернення зображення (якщо хочеш прямий FileResponse) ===
@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = IMAGES_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    return JSONResponse({"error": "File not found"}, status_code=404)


# === 404 для неіснуючих шляхів ===
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)


# === Запуск ===
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
