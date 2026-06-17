from sqlalchemy.orm import sessionmaker, joinedload

from datetime import date

from models import (
    engine,
    Department,
    Student,
    Course,
    Enrollment, 
    Professor
)

Session = sessionmaker(bind=engine)

session = Session()
 
# question 81
cs = Department(
    dept_name="Computer Science",
    head_of_dept="Dr. Ramesh Kumar",
    budget=850000
)

ec = Department(
    dept_name="Electronics",
    head_of_dept="Dr. Priya Nair",
    budget=620000
)

me = Department(
    dept_name="Mechanical",
    head_of_dept="Dr. Suresh Iyer",
    budget=540000
)

session.add_all([cs,ec,me])
session.commit()

print("Departments Inserted")


s1 = Student(
    first_name="Arjun",
    last_name="Mehta",
    email="arjun@college.edu",
    date_of_birth=date(2003, 4, 12),
    enrollment_year=2022,
    department=cs
)

s2 = Student(
    first_name="Priya",
    last_name="Suresh",
    email="priya@college.edu",
    date_of_birth=date(2003, 7, 25),
    enrollment_year=2022,
    department=cs
)

s3 = Student(
    first_name="Rohan",
    last_name="Verma",
    email="rohan@college.edu",
    date_of_birth=date(2002, 11, 8),
    enrollment_year=2021,
    department=ec
)

s4 = Student(
    first_name="Sneha",
    last_name="Patel",
    email="sneha@college.edu",
    date_of_birth=date(2004, 1, 30),
    enrollment_year=2023,
    department=me
)

s5 = Student(
    first_name="Vikram",
    last_name="Das",
    email="vikram@college.edu",
    date_of_birth=date(2003, 9, 14),
    enrollment_year=2022,
    department=cs
)

session.add_all([s1, s2, s3, s4, s5])

session.commit()

print("Students Inserted")

#82

c1 = Course(
    course_name="Data Structures",
    course_code="CS101",
    credits=4,
    department=cs
)

c2 = Course(
    course_name="Database Management Systems",
    course_code="CS102",
    credits=3,
    department=cs
)

c3 = Course(
    course_name="Circuit Theory",
    course_code="EC101",
    credits=3,
    department=ec
)

session.add_all([c1, c2, c3])

session.commit()

print("Courses Inserted")

e1 = Enrollment(
    student=s1,
    course=c1,
    enrollment_date=date.today(),
    grade="A"
)

e2 = Enrollment(
    student=s2,
    course=c2,
    enrollment_date=date.today(),
    grade="B"
)

e3 = Enrollment(
    student=s3,
    course=c3,
    enrollment_date=date.today(),
    grade="A"
)

e4 = Enrollment(
    student=s5,
    course=c1,
    enrollment_date=date.today(),
    grade="B"
)

session.add_all([e1, e2, e3, e4])

session.commit()

print("Enrollments Inserted")


#---------------------

students = session.query(Student).join(Department).filter(Department.dept_name == "Computer Science").all()

for s in students:
    print(s.first_name,s.last_name)


    
student = (session.query(Student).filter(Student.email == "arjun@college.edu").first())
student.enrollment_year = 2024
session.commit()

print("Updated")

#---------------------
enrollments = session.query(Enrollment).all()

for e in enrollments:
    print(f"id : {e.course_id} , Name :{e.student.first_name + e.student.last_name} , CourseName : {e.course.course_name})")

print(enrollments.count())

""" 
Step 84 Observation:

Using session.query(Enrollment).all()
and then accessing enrollment.student
and enrollment.course causes additional
queries for every enrollment.

This is the N+1 Query Problem.

Multiple SQL statements are generated
when related objects are loaded lazily.
 """

enrol_del =  session.query(Enrollment).first()

session.delete(enrol_del)
session.commit()

print("Enrollment deleted")



enrollments = session.query(Enrollment).all()

for e in enrollments:
    print(f"id : {e.course_id} , Name :{e.student.first_name + e.student.last_name} , CourseName : {e.course.course_name})")

"""
# Task 3

2026-06-17 14:25:10,112 INFO sqlalchemy.engine.Engine SELECT enrollments.enrollment_id AS enrollments_enrollment_id, enrollments.student_id AS enrollments_student_id, enrollments.course_id AS enrollments_course_id, enrollments.enrollment_date AS enrollments_enrollment_date, enrollments.grade AS enrollments_grade, students_1.student_id AS students_1_student_id, students_1.first_name AS students_1_first_name, students_1.last_name AS students_1_last_name, students_1.email AS students_1_email, students_1.date_of_birth AS students_1_date_of_birth, students_1.department_id AS students_1_department_id, students_1.enrollment_year AS students_1_enrollment_year, courses_1.course_id AS courses_1_course_id, courses_1.course_name AS courses_1_course_name, courses_1.course_code AS courses_1_course_code, courses_1.credits AS courses_1_credits, courses_1.max_seats AS courses_1_max_seats, courses_1.department_id AS courses_1_department_id 
FROM enrollments 
LEFT OUTER JOIN students AS students_1 ON students_1.student_id = enrollments.student_id 
LEFT OUTER JOIN courses AS courses_1 ON courses_1.course_id = enrollments.course_id
2026-06-17 14:25:10,113 INFO sqlalchemy.engine.Engine [generated in 0.00092s] {}
id : 2 , Name :PriyaSuresh , CourseName : Database Management Systems)
id : 3 , Name :RohanVerma , CourseName : Circuit Theory)
id : 1 , Name :VikramDas , CourseName : Data Structures)

N + 1 query has happened
"""


enrollments = session.query(Enrollment).options(
    joinedload(Enrollment.student),
    joinedload(Enrollment.course)
).all()

for e in enrollments:
    print(f"id : {e.course_id} , Name :{e.student.first_name} {e.student.last_name} , CourseName : {e.course.course_name}")


 
"""
================================================================================
STEP 90: PERFORMANCE BENCHMARK & METRIC COMPARISON (LAZY VS EAGER LOADING)
================================================================================
1. BASELINE CONFIGURATION (Lazy Loading - Task 2, Step 84)
   - Code: session.query(Enrollment).all()
   - Total Database Queries Fired: 7 SQL Queries
   - Under the Hood: 
     * 1 Initial query to scan the 'enrollments' table.
     * 6 Incremental emergency queries (2 per enrollment row) fired inside the 
       for-loop to lazily resolve 'e.student' and 'e.course' attributes.
   - Performance Impact: High latency overhead. This scales linearly to 
     (2N + 1) network roundtrips as rows grow.

2. OPTIMISED CONFIGURATION (Eager Loading - Task 3, Step 88)
   - Code: session.query(Enrollment).options(joinedload(Enrollment.student), joinedload(Enrollment.course)).all()
   - Total Database Queries Fired: 1 Single SQL Query
   - Under the Hood:
     * SQLAlchemy intercepts the query modifier and rewrites the command using 
       'LEFT OUTER JOIN students' and 'LEFT OUTER JOIN courses'.
     * Complete combined data payload is bundled into memory in 1 single trip.
   - Performance Impact: Instant loop execution with zero mid-loop DB calls. 
     Query footprint remains locked at exactly 1 query whether handling 3 rows 
     or 300,000 rows.
================================================================================
"""
