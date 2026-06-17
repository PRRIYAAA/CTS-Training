use college_db;

-- 35. Find all students who are enrolled in more courses than the average number of enrollments 
-- per student. (Use a non-correlated subquery to calculate the average.)

select s.student_id , s.first_name , s.last_name, count(e.course_id) as count_of_sub  from students s join enrollments e 
on e.student_id = s.student_id group by s.student_id , s.first_name , s.last_name  having count_of_sub > (
select avg(total_count) from 
	(
		select student_id , count(course_id) as total_count from enrollments group by student_id
	)
as temp
);

-- 36. List courses in which all enrolled students have received a grade of 'A'.
--  (Correlated subquery or NOT EXISTS.)

SELECT c.course_name
FROM courses c
JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
HAVING MIN(e.grade) = 'A'
   AND MAX(e.grade) = 'A';

-- 37. Find the professor with the highest salary in each department using a correlated subquery.
SELECT p1.prof_name , p1.salary
FROM professors p1
WHERE salary =
(
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p1.department_id = p2.department_id
);

-- 38. Using a subquery in the FROM clause (derived table), 
-- calculate the per-department average salary and then filter to departments where that average exceeds 85,000.

select * from 
( SELECT department_id,
           round(AVG(salary),2) AS avg_salary
    FROM professors
    GROUP BY department_id ) as dept_salary where avg_salary > 85000;
    

-- ------------------------------ TASK 2 -----------------------

-- 39. Create a view vw_student_enrollment_summary showing each student's full name, department, 
-- number of courses enrolled in, and GPA (average grade converted: A=4, B=3, C=2, D=1, F=0).

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    CONCAT(s.first_name,' ',s.last_name) AS student_name,
    d.dept_name,
    COUNT(e.course_id) AS total_courses,
    AVG(
        CASE
            WHEN e.grade='A' THEN 4
            WHEN e.grade='B' THEN 3
            WHEN e.grade='C' THEN 2
            WHEN e.grade='D' THEN 1
            WHEN e.grade='F' THEN 0
        END
    ) AS GPA
FROM students s
JOIN departments d
ON s.department_id = d.department_id
JOIN enrollments e
ON s.student_id = e.student_id
GROUP BY s.student_id,d.dept_name;

select * from vw_student_enrollment_summary

-- 40. Create a view vw_course_stats showing course_name, course_code, total_enrollments, and avg_gpa 
-- for each course.

CREATE VIEW vw_course_stats AS
select 
	c.course_name , c.course_code , 
	count(e.student_id) as total_enrollments , 
	AVG(
		CASE 
			WHEN e.grade='A' THEN 4
            WHEN e.grade='B' THEN 3
            WHEN e.grade='C' THEN 2
            WHEN e.grade='D' THEN 1
            WHEN e.grade='F' THEN 0
        END
    ) as avg_gpa 
    from courses c join enrollments e on c.course_id = e.course_id
    group by c.course_id ,  c.course_name;

select * from vw_course_stats

-- 41. Query vw_student_enrollment_summary to find students with GPA above 3.0.
select * from vw_student_enrollment_summary where gpa > 3.0;


-- 42. Attempt to UPDATE a row through vw_student_enrollment_summary and note what happens. Research and document in your comments why multi-table views are generally not updatable.
update vw_student_enrollment_summary set gpa = 2.0 where student_name = 'Arjun Mehta';

-- Multi-table views containing JOIN, GROUP BY,
-- aggregate functions such as COUNT and AVG
-- are generally not updatable because MySQL
-- cannot determine which underlying table row
-- should be modified.

-- 43. DROP both views and recreate vw_student_enrollment_summary as a view WITH CHECK OPTION  (use a single-table subset view for this step).

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    student_id,
    first_name,
    last_name,
    department_id
FROM students
WHERE department_id = 1
WITH CHECK OPTION;

drop view vw_student_enrollment_summary ;
DROP VIEW vw_course_stats;

-- ------------------------------ TASK 3 ---------------------------------

-- 44. Write a stored procedure sp_enroll_student (MySQL) or function fn_enroll_student (PostgreSQL) that 
-- accepts student_id, course_id, and enrollment_date, checks for duplicate enrollment, and inserts the 
-- record.

delimiter // 
create procedure sp_enroll_student(IN p_student_id int , p_course_id int, p_enrollment_date DATE)
begin
	IF EXISTS
    (
        SELECT *
        FROM enrollments
        WHERE student_id = p_student_id
        AND course_id = p_course_id
    )
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student already enrolled in this course';
        
	

    END IF;

end //
delimiter ;

call sp_enroll_student(1,1,'2022-07-01');

drop procedure sp_enroll_student;
select * from enrollments;

-- 45. Write a procedure sp_transfer_student that moves a student from one department to another. Wrap 
-- the UPDATE and a log-insert into a new table department_transfer_log inside a single transaction. 
-- ROLLBACK if either statement fails.

CREATE TABLE department_transfer_log
(
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE PROCEDURE sp_transfer_student
(
    IN p_student_id INT,
    IN p_new_department INT
)
BEGIN

    DECLARE v_old_department INT;

    START TRANSACTION;

    SELECT department_id
    INTO v_old_department
    FROM students
    WHERE student_id = p_student_id;

    UPDATE students
    SET department_id = p_new_department
    WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log
    (
        student_id,
        old_department,
        new_department
    )
    VALUES
    (
        p_student_id,
        v_old_department,
        p_new_department
    );

    COMMIT;

END $$

DELIMITER ;

-- 46. Test the transaction by manually introducing an error (e.g., invalid foreign key) and verify that the first 
-- UPDATE is also rolled back.

CALL sp_transfer_student(1,999);

-- 47. Use SAVEPOINT to create a mid-transaction checkpoint: insert two enrollment records; set a 
-- SAVEPOINT after the first; deliberately fail the second; ROLLBACK TO SAVEPOINT and verify only 
-- the first record was saved.

START TRANSACTION;

INSERT INTO enrollments
(student_id,course_id,enrollment_date)
VALUES
(1,5,'2025-01-01');

savepoint sp1;

INSERT INTO enrollments
(student_id,course_id,enrollment_date)
VALUES
(999,5,'2025-01-01');

rollback to sp1;
commit;

SELECT *
FROM enrollments
WHERE course_id = 5;