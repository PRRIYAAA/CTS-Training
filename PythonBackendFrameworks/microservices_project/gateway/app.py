from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

COURSE_URL = "http://localhost:5001"
STUDENT_URL = "http://localhost:5002"


@app.route('/api/courses', methods=['GET'])
def courses():

    response = requests.get(
        f"{COURSE_URL}/api/courses"
    )

    return jsonify(response.json())


@app.route('/api/courses/<path:path>',
           methods=['GET'])
def course_proxy(path):

    response = requests.get(
        f"{COURSE_URL}/api/courses/{path}"
    )

    return jsonify(response.json()), response.status_code


@app.route('/api/students',
           methods=['GET'])
def students():

    response = requests.get(
        f"{STUDENT_URL}/api/students"
    )

    return jsonify(response.json())


@app.route('/api/students/<int:id>/enroll',
           methods=['POST'])
def enroll(id):

    response = requests.post(
        f"{STUDENT_URL}/api/students/{id}/enroll",
        json=request.get_json()
    )

    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(port=5000, debug=True)