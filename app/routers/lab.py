import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select

from app.config import LAB_UPLOAD_PATH
from app.db import get_session
from app.models import LabData, User, LabWork
from app.utils import verify_access_token

router = APIRouter(tags=['lab'],
                   responses={404: {"description": "Not found"}})


@router.get('/get_lab_tasks')
def get_lab_tasks(session: Session = Depends(get_session)):
    return session.exec(select(LabData)).all()


@router.get('/get_lab_task/{course_id}')
def get_lab_task(course_id: int, user: User = Depends(verify_access_token),
                 session: Session = Depends(get_session)):
    if user.role == 'BAN':
        raise HTTPException(status_code=403)
    lab = session.exec(select(LabData).where(LabData.course_id == course_id)).first()
    return lab


@router.post('/pass_lab/{lab_data_id}')
async def pass_lab(lab_data_id: int,
                   file: UploadFile = File(...),
                   user: User = Depends(verify_access_token),
                   session: Session = Depends(get_session)
                   ):
    if user.role == 'BAN':
        raise HTTPException(status_code=403)

    lab_data = session.exec(select(LabData).where(LabData.id == lab_data_id)).first()
    if not lab_data:
        raise HTTPException(status_code=404)

    if not os.path.exists(LAB_UPLOAD_PATH):
        os.makedirs(LAB_UPLOAD_PATH)

    # Сохранение файла на сервере
    unique_filename = f"{uuid.uuid4()}_{file.filename}"  # Добавление UUID к имени файла
    file_path = os.path.join(LAB_UPLOAD_PATH, unique_filename)  # Полный путь к файлу
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Получение типа контента
    content_type = file.content_type

    # Создание записи в базе данных
    lab = LabWork(
        lab_data_id=lab_data_id,
        file_path=file_path,
        content_type=content_type,
        date_create=datetime.utcnow()
    )
    session.add(lab)
    session.commit()
    raise HTTPException(status_code=201)
