import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Numeric,
    Boolean,
    Time
)

from sqlalchemy.orm import (
    declarative_base,
    relationship
)

project_root = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_root / ".env")

db_driver = os.getenv("DB_DRIVER", "mysql+mysqlconnector")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD")
if not db_password:
    raise ValueError("DB_PASSWORD environment variable is required")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "college_db_orm")
db_echo = os.getenv("DB_ECHO", "True").lower() in ("1", "true", "yes")

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    db_url = DATABASE_URL
else:
    db_url = f"{db_driver}://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(
    db_url,
    echo=db_echo
)

Base = declarative_base()


# -------------------------
# Department
# -------------------------

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    dept_name = Column(
        String(100),
        nullable=False
    )

    head_of_dept = Column(
        String(100)
    )

    budget = Column(
        Numeric(12, 2)
    )

    students = relationship(
        "Student",
        back_populates="department"
    )

    courses = relationship(
        "Course",
        back_populates="department"
    )

    professors = relationship(
        "Professor",
        back_populates="department"
    )


# -------------------------
# Student
# -------------------------

class Student(Base):
    __tablename__ = "students"

    student_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = Column(
        String(50),
        nullable=False
    )

    last_name = Column(
        String(50),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    date_of_birth = Column(Date)

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    enrollment_year = Column(Integer)
    is_active = Column(Boolean , default= True)

    department = relationship(
        "Department",
        back_populates="students"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )
    

# -------------------------
# Course
# -------------------------

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    course_name = Column(
        String(150),
        nullable=False
    )

    course_code = Column(
        String(20),
        unique=True
    )

    credits = Column(Integer)

    max_seats = Column(
        Integer,
        default=60
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship(
        "Department",
        back_populates="courses"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )


# -------------------------
# Enrollment
# -------------------------

class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.student_id")
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.course_id")
    )

    enrollment_date = Column(Date)

    grade = Column(
        String(2)
    )

    student = relationship(
        "Student",
        back_populates="enrollments"
    )

    course = relationship(
        "Course",
        back_populates="enrollments"
    )


# -------------------------
# Professor
# -------------------------

class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    prof_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    salary = Column(
        Numeric(10, 2)
    )

    department = relationship(
        "Department",
        back_populates="professors"
    )

# -------------------------
# Course Schedule
# -------------------------

class CourseSchedule(Base):
    __tablename__ = "course_schedules"
    schedule_id = Column(Integer, primary_key=True)
    day_of_week = Column(Integer ,  ForeignKey("courses.course_id"))
    start_time = Column(Time)
    end_time = Column(Time)





# -------------------------
# Test Connection
# -------------------------

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables Created Successfully")