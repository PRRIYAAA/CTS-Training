from sqlalchemy import func, and_ , or_
from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Department, Student, Course, Enrollment, Professor

Session = sessionmaker(bind=engine)
session = Session()

print("==== RUNNING READ QUERIES ====\n")

# ----------------------------------------------------
# Write your Problem 1 code here:
# ----------------------------------------------------

""" student = session.query(Student).filter(Student.email.like("arjun%")).all()
for s in student:
    print(s.first_name,s.last_name,s.mail) """

# ----------------------------------------------------
# Write your Problem 2 code here:
# ----------------------------------------------------   
""" dept = (
    session.query(Department)
    .filter(
        and_(
            Department.budget >= 600000, 
            Department.dept_name != 'Mechanical' # direct != is cleaner than not_()
        )
    )
    .order_by(Department.budget.desc()) # Proper sorting syntax
    .all()
)

print("\n===============================")

for d in dept:
    # d.courses will work perfectly because of your relationship setup!
    print(f"ID: {d.department_id} | Name: {d.dept_name} | Budget: {d.budget}") """
    

# ----------------------------------------------------
# Write your Problem 3 code here:
# ----------------------------------------------------   

""" dept = (
    session.query(Student).join(Department).filter(
        Department.dept_name == "Electronics"
    ).all()
)


for d in dept:
    print(d.first_name,d.last_name,d.department.dept_name) """


# 1. Import func at the top of your file
from sqlalchemy import func

# 2. Select the Department Name and the Count of Courses
course_counts = (
    session.query(
        Department.dept_name, 
        func.count(Course.course_id).label("total_courses") # Counts the items
    )
    .join(Course) # Joins the tables together
    .group_by(Department.dept_name) # Groups them by department
    .all()
)

# 3. Loop through the result tuples
for dept_name, count in course_counts:
    print(f"Department: {dept_name} | Total Courses: {count}")
