from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean

class Base(DeclarativeBase):
    pass

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    credits = Column(Integer)
    department_id = Column(Integer)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key= True)
    name = Column(String)
    email = Column(String)

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True) 
    student_id = Column(Integer) 
    course_id = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)