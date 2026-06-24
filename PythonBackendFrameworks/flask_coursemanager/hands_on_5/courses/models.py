from app import db

class Department(db.Model):

    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    courses = db.relationship(
        'Course',
        back_populates='department'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    description = db.Column(db.String(200))

    department_id = db.Column(
        db.Integer,
        db.ForeignKey('departments.id')
    )

    department = db.relationship(
        'Department',
        back_populates='courses'
    )

    enrollments = db.relationship(
        'Enrollment',
        back_populates='course'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "department_id": self.department_id
        }

class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    enrollments = db.relationship(
        'Enrollment',
        back_populates='student'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

class Enrollment(db.Model):

    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id')
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id')
    )

    student = db.relationship(
        'Student',
        back_populates='enrollments'
    )

    course = db.relationship(
        'Course',
        back_populates='enrollments'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id
        }