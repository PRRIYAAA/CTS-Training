from flask import Flask, jsonify, request
import requests
from requests.exceptions import ConnectionError

app = Flask(__name__)

students = [
    {
        "id": 1,
        "name": "Priya"
    }
]

enrollments = []

@app.route('/api/students')
def get_students():
    return jsonify(students)


@app.route('/api/students/<int:id>/enroll', methods=['POST'])
def enroll(id):

    data = request.get_json()

    course_id = data.get("course_id")

    try:

        response = requests.get(
            f"http://localhost:5001/api/courses/{course_id}"
        )

        if response.status_code != 200:
            return jsonify({
                "message": "Course does not exist"
            }), 404

    except ConnectionError:

        return jsonify({
            "message":
            "Course Service unavailable"
        }), 503

    enrollments.append({
        "student_id": id,
        "course_id": course_id
    })

    return jsonify({
        "message": "Enrollment successful"
    })


if __name__ == "__main__":
    app.run(port=5002, debug=True)