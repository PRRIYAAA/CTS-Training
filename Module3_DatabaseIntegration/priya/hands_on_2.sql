-- departments
INSERT INTO departments (dept_name, head_of_dept, budget) VALUES
  ('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
  ('Electronics', 'Dr. Priya Nair', 620000.00),
  ('Mechanical', 'Dr. Suresh Iyer', 540000.00),
  ('Civil', 'Dr. Ananya Sharma', 430000.00);
  
-- students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, 
enrollment_year) VALUES
  ('Arjun',  'Mehta',    'arjun.mehta@college.edu',    '2003-04-12', 1, 2022),
  ('Priya',  'Suresh',   'priya.suresh@college.edu',   '2003-07-25', 1, 2022),
  ('Rohan',  'Verma',    'rohan.verma@college.edu',    '2002-11-08', 2, 2021),
  ('Sneha',  'Patel',    'sneha.patel@college.edu',    '2004-01-30', 3, 2023),
  ('Vikram', 'Das',      'vikram.das@college.edu',     '2003-09-14', 1, 2022),
  ('Kavya',  'Menon',    'kavya.menon@college.edu',    '2002-05-17', 2, 2021),
  ('Aditya', 'Singh',    'aditya.singh@college.edu',   '2004-03-22', 4, 2023),
  ('Deepika','Rao',      'deepika.rao@college.edu',    '2003-08-09', 1, 2022);

-- courses
INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
  ('Data Structures & Algorithms', 'CS101', 4, 1),
  ('Database Management Systems',  'CS102', 3, 1),
  ('Object Oriented Programming',  'CS103', 4, 1),
  ('Circuit Theory',               'EC101', 3, 2),
  ('Thermodynamics',               'ME101', 3, 3);

-- enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
  (1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
  (2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
  (3, 4, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
  (5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
  (6, 4, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
  (8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');


INSERT INTO professors (prof_name, email, department_id, salary) VALUES
  ('Dr. Anand Krishnan',  'anand.k@college.edu',   1, 95000.00),
  ('Dr. Meena Pillai',    'meena.p@college.edu',   1, 88000.00),
  ('Dr. Sunil Rajan',     'sunil.r@college.edu',   2, 82000.00),
  ('Dr. Latha Gopal',     'latha.g@college.edu',   3, 79000.00),
  ('Dr. Kartik Bose',     'kartik.b@college.edu',  4, 76000.00);

-- Additional  2 members
INSERT INTO students
(first_name,last_name,email,date_of_birth,department_id,enrollment_year)
VALUES
('Rahul','Kumar','rahul.kumar@college.edu','2003-06-15',1,2022),
('Anjali','Sharma','anjali.sharma@college.edu','2004-02-20',2,2023);

select count(*) from students;
select count(*) from courses;
select count(*) from enrollments;
select count(*) from professors;
select count(*) from departments;

update enrollments set grade = 'B' where student_id = 5 and course_id = 1;

SELECT * FROM enrollments WHERE grade IS NULL;

-- for safe mode  
SET SQL_SAFE_UPDATES = 1;

delete from enrollments where grade IS NULL;

-- ============================================== --
--                  Task 2 						  --
-- ============================================== --

select first_name , last_name from students where enrollment_year = 2022 order by last_name;

select * from courses where credits > 3 order by credits desc;

select * from professors where salary >= 80000 and salary <= 95000;

select * from students where email LIKE '%@college.edu';

select enrollment_year,count(*) as number_of_students from students group by enrollment_year;

-- ============================================== --
--                  Task 3     					  --
-- ============================================== --

select concat(s.first_name , ' ' ,s.last_name) as full_name , d.dept_name from students s join departments d 
where s.department_id = d.department_id;

SELECT CONCAT(s.first_name,' ',s.last_name) AS full_name,
       c.course_name
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
JOIN courses c
ON e.course_id = c.course_id;

SELECT s.student_id,
       CONCAT(s.first_name,' ',s.last_name) AS student_name
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id 
where e.student_id is NULL;

SELECT c.course_name,
       COUNT(e.student_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

-- List each department along with its professors and their salaries. Include departments that have no 
-- professors yet

select d.dept_name , p.prof_name , p.salary from departments d left join professors p 
on d.department_id = p.department_id;  

-- ============================================== --
--                  Task 4     					  --
-- ============================================== --

-- Calculate the total number of enrollments per course. Display course_name and enrollment_count.
select c.course_name , count(e.enrollment_id) as enrollment_count from courses c join enrollments e 
on c.course_id = e.course_id group by c.course_id, c.course_name;

--  Find the average salary of professors per department. Round to 2 decimal places.
select d.dept_name , round(avg(p.salary),2) as avg_salary from departments d join professors p 
on d.department_id = p.department_id group by d.department_id, d.dept_name;

--  Find all departments where the total budget exceeds 600,000
select * from departments where budget > 600000;

-- Show the grade distribution for course CS101: count of each grade (A, B, C, D, F).
select e.grade , count(*) as count from enrollments e join courses c on c.course_id = e.course_id
where course_code = 'CS101' group by e.grade;

-- Using HAVING, list departments where more than 2 students are enrolled across all courses in that department.
SELECT d.dept_name,
       COUNT(s.student_id) AS total_students
FROM departments d
JOIN students s
ON d.department_id = s.department_id
GROUP BY d.department_id, d.dept_name
HAVING COUNT(s.student_id) > 2;