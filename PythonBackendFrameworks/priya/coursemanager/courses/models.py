from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=50)
    head_of_dept = models.CharField(max_length=10)
    budget = models.DecimalField(max_digits=12,decimal_places=2)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField()
    department = models.ForeignKey(Department, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete = models.CASCADE)
    enrollment_year = models.IntegerField()

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    enrollment_date = models.DateField()
    grade = models.CharField(max_length=5,null=True,blank=True)

    def __str__(self):
        return f"{self.student} - {self.course}"
    
    class Meta:
        unique_together = [
            ['student', 'course']
        ]

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username



