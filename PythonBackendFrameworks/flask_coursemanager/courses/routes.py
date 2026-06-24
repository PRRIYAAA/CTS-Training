from flask import Blueprint, request, jsonify

courses_bp = Blueprint("courses", __name__, url_prefix = "/api/courses")

def make_response_json(data, status_code):

    return jsonify({
        "status": "success",
        "data": data
    }), status_code


courses = []

# Get all the  courses
@courses_bp.route("/", methods=["GET"])
def get_courses():
    return make_response_json(courses, 200)


#Create courses
@courses_bp.route("/", methods=["POST"])
def create_course():
    data = request.get_json()
    if data is None:
        return jsonify({
            "error" : "Request body must be JSON"
        }), 400

    required_fields = ["name" , "code", "credits"]
    for field in required_fields:

        if field not in data:

            return jsonify({
                "error": f"{field} is required"
            }), 400

    course = {
        "id": len(courses) + 1,
        "name": data.get("name"),
        "code": data.get("code"),
        "credits": data.get("credits")
    }

    courses.append(course)

    return make_response_json(course, 201)

#Get the course by id
@courses_bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):
    for course in courses:
        if course["id"] == course_id:
            return make_response_json(course, 200)

    return jsonify({"error" : "Data not found"}, 400)

#update the course by id
@courses_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):

    data = request.get_json()

    for course in courses:

        if course["id"] == course_id:

            course["name"] = data.get("name",course["name"])

            course["code"] = data.get("code",course["code"])

            course["credits"] = data.get("credits",course["credits"])

            return make_response_json(course,200)

    return jsonify({"error": "Course not found"}), 404

#delete the course by id
@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):

    data = request.get_json()
    for course in courses:
        if course["id"] == course_id:
            data.remove(course)
            return jsonify({"message": "Course deleted"}), 200

    
    return jsonify({"message": "Course not found"}), 404
    

