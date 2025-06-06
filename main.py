from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from db import model
from db.database import engine, Base
from fastapi.responses import HTMLResponse
from router import advertisement, category,image,chat
from router.rating import router as rating_router   
from router.auth import router as auth_router
from router import chat
from router import transactions

app = FastAPI()
app.mount("/images", StaticFiles(directory="uploaded_images"), name="images")
UPLOAD_DIR = "uploaded_images"

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
Base.metadata.create_all(bind=engine)  # Create tables on startup

app.include_router(auth_router, prefix="/auth", tags=["Registration"])
app.include_router(category.router)
app.include_router(advertisement.router)
app.include_router(image.router)
app.include_router(chat.router)
app.include_router(rating_router)
app.include_router(transactions.router)

