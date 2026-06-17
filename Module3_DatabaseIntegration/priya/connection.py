""" 
56. Simulate the N+1 problem in Python: fetch all enrollments with SELECT * FROM enrollments, then 
loop through each row and issue a separate SELECT to fetch the student's name. Count the total 
queries executed.

import mysql.connector
import time

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="YOUR_PASSWORD",
    database="college_db"
)

cursor = conn.cursor()

start = time.time()

query_count = 0

cursor.execute("SELECT * FROM enrollments")
query_count += 1

enrollments = cursor.fetchall()

for enrollment in enrollments:

    student_id = enrollment[1]

    cursor.execute(
        "SELECT first_name FROM students WHERE student_id=%s",
        (student_id,)
    )

    cursor.fetchone()

    query_count += 1

end = time.time()

print("N+1 Version")
print("Queries Executed:", query_count)
print("Execution Time:", end - start)

conn.close()

"""

"""
57. Rewrite the script using a single JOIN query that retrieves all enrollment records with student names in 
one query.
"""
import mysql.connector
import time

# Use environment variable for password - DO NOT hardcode credentials
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),  # Set this in .env file
    database=os.getenv("DB_NAME", "college_db")
)

cursor = conn.cursor()

start = time.time()

cursor.execute("""
SELECT
    e.enrollment_id,
    s.first_name,
    s.last_name,
    e.course_id
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
""")

rows = cursor.fetchall()

query_count = 1

end = time.time()

print("JOIN Version")
print("Queries Executed:", query_count)
print("Execution Time:", end - start)

conn.close()