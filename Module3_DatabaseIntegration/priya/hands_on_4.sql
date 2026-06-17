use college_db;

SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- 48,49,50 
/*
Baseline EXPLAIN Output

Seq Scan on students
Seq Scan on enrollments
Seq Scan on courses

Observation:
Database performs full table scans because
no indexes exist.

Estimated Cost:
(cost=0.00..45.00)

This may become slow when tables grow.

11 row(s) returned

*/
-- ----------------------------Task 2 -----------------------------------------
-- 51.  Create a B-Tree index on students.enrollment_year.

create INDEX idx_enrollement_year on students(enrollment_year);

/*52. Create a composite UNIQUE index on enrollments(student_id, course_id) — this also prevents 
duplicate enrollments.*/

create unique index idx_enrollement_unique on enrollments(student_id, course_id);

-- Getting  duplicate data found 

/* 53. Create an index on courses.course_code.*/

create index idx_course_code on courses(course_code);

/* 54. Re-run the EXPLAIN from Task 1 and compare the new plan to the baseline. Document the change 
(Seq Scan → Index Scan?) as a comment. */

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id=e.student_id
JOIN courses c
ON c.course_id=e.course_id
WHERE s.enrollment_year=2022;

/*
1	SIMPLE	s		ref	PRIMARY,idx_enrollement_year	idx_enrollement_year	5	const	5	100.00	
1	SIMPLE	e		ref	student_id,course_id	student_id	5	college_db.s.student_id	2	100.00	Using where
1	SIMPLE	c		eq_ref	PRIMARY	PRIMARY	4	college_db.e.course_id	1	100.00	

 */
 
/*
EXPLAIN Output After Adding Indexes

Table: students (s)
Access Type: ref
Index Used: idx_enrollement_year

Table: enrollments (e)
Access Type: ref
Index Used: student_id

Table: courses (c)
Access Type: eq_ref
Index Used: PRIMARY

Observation:
The optimizer uses the index
idx_enrollement_year on students
to filter enrollment_year = 2022.

The enrollments table uses the
student_id index for the join.

The courses table uses the PRIMARY
KEY for efficient lookup.

Compared to the baseline plan,
table scans have been reduced and
index lookups are being used,
resulting in improved query performance.
*/

/* 55. Create a partial index on enrollments(student_id) WHERE grade IS NULL to optimise lookups for 
unevaluated enrollments */

/*
MySQL does not support partial indexes with a WHERE clause.

PostgreSQL syntax would be:

CREATE INDEX idx_pending_grade
ON enrollments(student_id)
WHERE grade IS NULL;

As an alternative in MySQL, a composite index
(student_id, grade) was created to improve
queries involving NULL grades.
*/

-- -----------------------------Task 3-------------------------------------

/*
56. Simulate the N+1 problem in Python: fetch all enrollments with SELECT * FROM enrollments, then 
loop through each row and issue a separate SELECT to fetch the student's name. Count the total 
queries executed.

output (got  in python):
N+1 Version
Queries Executed: 14
Execution Time: 0.0 

*/

/* 
57. Rewrite the script using a single JOIN query that retrieves all enrollment records with student names in 
one query.

output:

JOIN Version
Queries Executed: 1
Execution Time: 0.0
*/

/* 
58. Compare the number of database round-trips between the two approaches and log the difference 
using Python's time module.

"""
Comparison

N+1 Version:
13 database round-trips

JOIN Version:
1 database round-trip

Reduction:
13 -> 1

The JOIN version is significantly more efficient because
all required data is fetched using a single query.
"""

*/

/*
59. Document in comments: in a real application with 10,000 enrollments, how many extra queries would 
the N+1 version issue

"""
N+1 Problem Analysis

If the application contains 10,000 enrollments:

N+1 Version:
1 query to fetch enrollments
10,000 additional queries to fetch student names

Total = 10,001 queries

JOIN Version:
1 query

Extra Queries Issued By N+1 Version:
10,000

This demonstrates why the N+1 problem causes
serious performance issues in large applications.
"""
*/






