from fastapi import FastAPI, Depends, HTTPException, Request, status, Response, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from typing import Optional
from database import get_db, engine
from models import Base, Course, Student, Enrollment, User
from schemas import *
from security import get_password_hash

""" @app.get("/")
def home():
    return {"message": "API running"}


@app.post("/api/courses/")
async def create_course(course : CourseCreate):
    return {
        "message" : "Course added",
        "course" : course
    }

@app.get("/api/courses/{course_id}")
async def get_courses(course_id : int):
    return {
        "course_id" : course_id
    }

@app.get("/api/courses/")
async def get_courses(skip: int = 0,limit: int = 10,department_id: int | None = None):
    return {
        "skip": skip,
        "limit": limit,
        "department_id": department_id
    }

"""

app = FastAPI(
    title="Course Management API",
    description="""
    A FastAPI application for managing courses,
    students, and enrollments.

    Features:
    - Course CRUD
    - Student CRUD
    - Enrollment Management
    - Background Tasks
    - Async SQLAlchemy
    """,
    version="1.0.0",
    contact={
        "name": "Priyadharshini K",
        "email": "fromkpriyadharshini@example.com"
    }
)


# ==================================================
# Background Task
# Purpose : Simulates sending an enrollment
#           confirmation email.
# ==================================================
def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")


@app.post(
    "/api/v1/auth/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    
    # Check whether email already exists
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password before storing
    try:
        hashed_password = get_password_hash(user.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid password: {exc}"
        )

    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


# Create tables automatically when server starts
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Root Route - Check if API is running
@app.get("/")
async def home():
    return {"message": "API running"}


# Create a new course
@app.post("/api/v1/courses/", response_model= CourseResponse , status_code= status.HTTP_201_CREATED, tags=["Courses"], 
    summary="Create a new course",
    response_description="Successfully created course")
async def create_course(response : Response, course: CourseCreate,db: AsyncSession = Depends(get_db)):
    new_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )

    db.add(new_course)

    await db.commit()
    await db.refresh(new_course)
    response.headers['Location'] = f"/api/courses/{new_course.id}"
    return new_course


# Get all courses with pagination and filtering by department
@app.get("/api/v1/courses")
async def get_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Course)

    if search:
        query = query.where(
            Course.name.ilike(f"%{search}%") |
            Course.code.ilike(f"%{search}%")
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    offset = (page - 1) * page_size

    result = await db.execute(
        query.offset(offset).limit(page_size)
    )

    courses = result.scalars().all()

    return {
        "count": total,
        "next": None,
        "previous": None,
        "results": courses
    }


# Get a single course by ID
@app.get("/api/v1/courses/{course_id}", response_model = CourseResponse, tags=["Courses"],status_code = status.HTTP_200_OK)
async def get_course(course_id : int , db : AsyncSession = Depends(get_db)): 
    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


# Update an existing course by ID
@app.put("/api/v1/courses/{course_id}", response_model= CourseResponse, tags=["Courses"],status_code = status.HTTP_200_OK)
async def update_course(
    course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    db_course = result.scalar_one_or_none()

    if not db_course:
        raise HTTPException(
        status_code=404,
        detail="Course not found"
)

    if course.name is not None:
        db_course.name = course.name

    if course.code is not None:
        db_course.code = course.code

    if course.credits is not None:
        db_course.credits = course.credits

    if course.department_id is not None:
        db_course.department_id = course.department_id

    await db.commit()
    await db.refresh(db_course)

    return db_course

# Patch the record of a course by ID
@app.patch("/api/v1/courses/{course_id}", response_model= CourseResponse, tags=["Courses"], status_code = status.HTTP_200_OK)
async def patch_course(
    course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    db_course = result.scalar_one_or_none()

    if not db_course:
        raise HTTPException(
        status_code=404,
        detail="Course not found"
)

    update_data = course.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_course, key, value)

    await db.commit()
    await db.refresh(db_course)

    return db_course


# Delete a course by ID
@app.delete("/api/v1/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    
    

    await db.delete(course)
    await db.commit()

    return Response(status = 204)


# Get all students enrolled in a specific course
@app.get("/api/v1/courses/{id}/students", tags=["Courses"], status_code = status.HTTP_200_OK)
async def get_course_students(id : int , db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student)
        .join(Enrollment,  Student.id == Enrollment.student_id)
    .where(Enrollment.course_id == id))

    return result.scalars().all()

# ----------------------------- STUDENT---------------------------------------------

# Create a new student
@app.post(
    "/api/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
    
)
async def create_student(
    response : Response,
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    new_student = Student(
        name=student.name,
        email=student.email
    )

    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    response.headers['Location'] = f"/api/students/{new_student.id}"

    return new_student


    
# Get a single student by ID
@app.get(
    "/api/students/{id}",
    response_model=StudentResponse,
    tags=["Students"], status_code = status.HTTP_200_OK
)
async def get_student(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Student).where(Student.id == id)
    )

    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

# Update an existing student by ID
@app.put(
    "/api/students/{id}",
    response_model=StudentResponse,
    tags=["Students"], status_code = status.HTTP_200_OK
)
async def update_student(
    id: int,
    student: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Student).where(Student.id == id)
    )

    db_student = result.scalar_one_or_none()

    if not db_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if student.name is not None:
        db_student.name = student.name

    if student.email is not None:
        db_student.email = student.email

    await db.commit()
    await db.refresh(db_student)

    return db_student


# Delete a student by ID
@app.delete(
    "/api/students/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"]
)
async def delete_student(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Student).where(Student.id == id)
    )

    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    await db.delete(student)
    await db.commit()


# Create a new student enrollment in a course
# ==================================================
# Create Enrollment
# Method  : POST
# Endpoint: /api/enrollments/
# Purpose : Enroll a student into a course and
#           send confirmation email in background.
# ==================================================
@app.post(
    "/api/enrollments/",
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(
    response: Response,
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):

    # Check Student Exists
    student_result = await db.execute(
        select(Student).where(
            Student.id == enrollment.student_id
        )
    )

    student = student_result.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )

    db.add(new_enrollment)

    await db.commit()
    await db.refresh(new_enrollment)

    # Background Task
    background_tasks.add_task(
        send_confirmation_email,
        student.email
    )
    response.headers['Location'] = f"/api/enrollments/{new_enrollment.id}"

    return new_enrollment


# Get all enrollments
@app.get("/api/enrollments/", tags=["Enrollments"], status_code = status.HTTP_200_OK)
async def get_enrollments(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Enrollment)
    )

    return result.scalars().all()

# Get a single enrollment by ID
@app.get("/api/enrollments/{id}", tags=["Enrollments"], status_code = status.HTTP_200_OK)
async def get_enrollment(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Enrollment)
        .where(Enrollment.id == id)
    )

    enrollment = result.scalar_one_or_none()

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return enrollment


# Update an existing enrollment by ID
@app.put("/api/enrollments/{id}", tags=["Enrollments"], status_code = status.HTTP_200_OK)
async def update_enrollment(
    id: int,
    enrollment: EnrollmentCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Enrollment)
        .where(Enrollment.id == id)
    )

    db_enrollment = result.scalar_one_or_none()

    if not db_enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    db_enrollment.student_id = enrollment.student_id
    db_enrollment.course_id = enrollment.course_id

    await db.commit()
    await db.refresh(db_enrollment)

    return db_enrollment


# delete an existing enrollment by ID
@app.delete(
    "/api/enrollments/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"]
)
async def delete_enrollment(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Enrollment)
        .where(Enrollment.id == id)
    )

    enrollment = result.scalar_one_or_none()

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    await db.delete(enrollment)
    await db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

"""
ARCHITECTURE DISCUSSION: THE TWO MAJOR VERSIONING STRATEGIES

   1. URL Path Versioning (The Implementation Task)
   In this approach, the version number is hardcoded directly into the web path.

    Example Route: GET /api/v1/courses/
      * How it works: The routing system of your backend framework handles it like
       a completely separate folder path. 


   2. Header-Based Versioning (The Alternative)

   In this approach, the URL remains completely clean and never changes. The
   client must instead pass a custom token inside the HTTP request headers to
   ask for a specific version.


   * Example Route: GET /api/courses/
   * Example Request Header: Accept: application/vnd.api+json;version=1
   * How it works: Your backend routing logic reads the incoming request
    metadata, checks the Accept string, and forwards the traffic to the
    correct Python controller function based on that number.
      """ 
