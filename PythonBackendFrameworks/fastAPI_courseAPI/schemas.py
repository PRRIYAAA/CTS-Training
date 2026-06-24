from pydantic import BaseModel, EmailStr, Field
from typing import Optional,List


class CourseCreate(BaseModel):
    name : str
    code : str
    credits : int
    department_id : int 


class CourseUpdate(BaseModel):
    name : Optional[str] = None
    code : Optional[str] = None
    credits : Optional[int] = None
    department_id : Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    class Config:
        from_attributes = True


class DepartmentResponse(BaseModel):
    id: int
    name: str
    courses: List[CourseResponse] = []

#student 

class StudentCreate(BaseModel):
    name: str
    email: str

class StudentUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True



