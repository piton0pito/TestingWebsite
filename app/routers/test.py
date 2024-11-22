from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import Test, User
from app.schemas import GetTestByName, GetTestByCourse, AnswerTest
from app.utils import verify_access_token

router = APIRouter(tags=['user'],
                   responses={404: {"description": "Not found"}})


@router.post('/get_tests/title_topic')
def get_courses(data: GetTestByName, session: Session = Depends(get_session)):
    query = select(Test)

    if data.title != 'None':
        query = query.where(Test.title == data.title)
    if data.topic != 'None':
        query = query.where(Test.topic == data.topic)

    offset = data.offset
    limit = data.limit
    query = query.offset(offset).limit(limit)

    tests = session.exec(query).all()
    return tests


@router.post('/get_tests/course_id')
def get_courses(data: GetTestByCourse, session: Session = Depends(get_session)):
    query = select(Test).where(Test.courses_id == data.course_id)

    offset = data.offset
    limit = data.limit
    query = query.offset(offset).limit(limit)

    tests = session.exec(query).all()
    return tests


@router.get('/get_test/{test_id}')
def get_course_data(test_id: int, user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
    if user.role == 'BAN':
        raise HTTPException(status_code=403)
    test = session.exec(select(Test).where(Test.id == test_id)).first()
    if not test:
        raise HTTPException(status_code=404)
    return test


@router.post('/answer_test/{test_id}')
def answer_test(test_id: int, data: AnswerTest, user: User = Depends(verify_access_token), session: Session = Depends(get_session)):
    test = session.exec(select(Test).where(Test.id == test_id)).first()
    if not test:
        raise HTTPException(status_code=404)

    for test_data in test.data:
        print(test_data.true_answer)
        if test_data.true_answer == data.answer:
            return {"message": "Correct answer"}
        else:
            return {"message": "No correct answer"}


