create database college_db;

USE college_db;

create table students (
	student_id INT primary key Auto_increment,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    email varchar(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT, 
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

create table departments(
	department_id INT Primary key auto_increment,
    dept_name varchar(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

create table courses(
	course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    foreign key(department_id) references departments(department_id)
);

create table enrollments(
	enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
	student_id INT,
	course_id INT,
	enrollment_date DATE,
	grade CHAR(2),
	foreign key (student_id) references students(student_id),
	foreign key (course_id) references courses(course_id)
);

create table professors(
	professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    foreign key(department_id) references departments(department_id)
    
);

-- =====================================================
-- NORMALIZATION ANALYSIS (1NF, 2NF, 3NF)
-- =====================================================

-- 1NF (First Normal Form)
-- All tables satisfy 1NF because each column stores atomic values.
-- There are no repeating groups or multi-valued attributes.
-- For example, storing multiple phone numbers in a single column
-- such as '9876543210,8765432109' would violate 1NF.

-- 2NF (Second Normal Form)
-- All non-key attributes are fully dependent on their primary keys.
-- In the enrollments table, a candidate key can be
-- (student_id, course_id). Attributes such as enrollment_date
-- and grade depend on the complete combination of student_id
-- and course_id, not on only one part of the key.
-- Therefore, the schema satisfies 2NF.

-- 3NF (Third Normal Form)
-- The schema contains no transitive dependencies.
-- For example, dept_name is stored in the departments table
-- and not in the students table.
-- If dept_name were stored in students, it would depend on
-- department_id rather than directly on student_id,
-- causing a transitive dependency and violating 3NF.
-- Therefore, the schema satisfies 3NF.

-- 3NF Analysis for Enrollments Table
-- The enrollments table contains enrollment_id, student_id,
-- course_id, enrollment_date, and grade.
-- enrollment_date and grade depend directly on the enrollment.
-- No non-key attribute depends on another non-key attribute.
-- Hence, there are no transitive dependencies in enrollments.
-- Therefore, the enrollments table is in 3NF.


-- =====================================================
-- TASK 3 : ALTER AND EXTEND THE SCHEMA
-- =====================================================

-- Step 10: Add phone_number column to students table
ALTER TABLE students
ADD phone_number VARCHAR(15);

-- Step 11: Add max_seats column to courses table
ALTER TABLE courses
ADD max_seats INT DEFAULT 60;

-- Step 12: Add CHECK constraint for grades
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

-- Step 13: Rename hod_name to head_of_dept
ALTER TABLE departments
CHANGE hod_name head_of_dept VARCHAR(100);

-- Step 14: Drop phone_number column (schema rollback)
ALTER TABLE students
DROP COLUMN phone_number;

-- Verify changes
DESC students;
DESC courses;
DESC departments;
DESC enrollments;



