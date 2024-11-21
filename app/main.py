from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from sqlmodel import SQLModel
from starlette.responses import FileResponse

from app.db import engine
from app.routers import user, course
from app.utils import send_mail, get_meme

if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(course.router)
# app.include_router(reviews.router)
# app.include_router(message.router)
# app.include_router(admin.router)


@app.get('/mem/')
def get():
    raise HTTPException(status_code=418)


@app.post("/send-email")
def schedule_mail(email: str, code: str, tasks: BackgroundTasks):
    send_mail(email, code)
    raise HTTPException(status_code=200, detail='Email has been scheduled')


@app.get("/random_meme")
async def get_image():
    await get_meme()
    image_path = Path("../test/meme.jpg")  # Replace with the actual image path
    return FileResponse(image_path, media_type="image/jpeg")


if __name__ == '__main__':
    uvicorn.run(app, port=8001)