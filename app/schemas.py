import json
from datetime import datetime
from typing import Dict, Any, Optional, List

from pydantic import BaseModel, EmailStr
from sqlmodel import Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.models import TestData, CompletedCourses


class UserCreate(BaseModel):
    email: EmailStr = Field(default='Email')  # почта
    phone: PhoneNumber = Field(default='+78005553535')
    name: str = Field(default='Имя')  # имя
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')


class UserUpdate(BaseModel):
    email: EmailStr = Field(default='Email')
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')


class CreateNewPassword(BaseModel):
    email: EmailStr = Field(default='Email')
    code: str = Field(default='Verify code')
    password: str = Field(default='Password')
    complete_password: str = Field(default='Confirm the password')


class GetUser(BaseModel):
    email: EmailStr = Field(default='Email')  # почта
    name: str = Field(default='Имя')  # имя
    completed_courses: Optional[List[CompletedCourses]]


class AddUpdateCourse(BaseModel):
    title: str
    topic: str
    data: str


class GetCourse(BaseModel):
    title: str = Field(default=None)
    topic: str = Field(default=None)
    offset: int = Field(default=0, description='offset')
    limit: int = Field(default=10, description='limit')


class AddUpdateTest(BaseModel):
    title: str
    topic: str
    data: TestData


class GetTestByName(BaseModel):
    title: str = Field(default=None)
    topic: str = Field(default=None)
    offset: int = Field(default=0, description='offset')
    limit: int = Field(default=10, description='limit')


class GetTestByCourse(BaseModel):
    course_id: int
    offset: int = Field(default=0, description='offset')
    limit: int = Field(default=10, description='limit')


class AnswerTest(BaseModel):
    answer: str


class GetVideoByName(BaseModel):
    title: str = Field(default=None)
    topic: str = Field(default=None)
    offset: int = Field(default=0, description='offset')
    limit: int = Field(default=10, description='limit')


class GetVideoByCourse(BaseModel):
    course_id: int
    offset: int = Field(default=0, description='offset')
    limit: int = Field(default=10, description='limit')


class ReturnVideoSearch(BaseModel):
    course_id: int
    title: str
    topic: str
    date_create: datetime
    date_last_update: datetime




class CreateUpdateMessage(BaseModel):
    recipient_user_id: int
    message: str = Field(default='message')






class Email(BaseModel):
    email: str
