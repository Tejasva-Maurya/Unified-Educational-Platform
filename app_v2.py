from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

import all_functions_v1 as af
import aggregrate_v3 as aggregrate_v2
import create_folder

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://void050710:Voiduep050710@void-uep.guig8vk.mongodb.net/?retryWrites=true&w=majority"
)
db = client["CREDENTIALS"]
student_collection = db["Students_Cred"]
teacher_collection = db["Teachers_Cred"]
courses_collection = db["Courses"]
groups_collection = db["Groups"]
folders_collection = db["folder_id"]

global_user_id = None
global_user_type = None


@app.route("/")
def index():
    # checking if file exist or not
    if os.path.isfile("token.json"):
        # os.remove() function to remove the file
        os.remove("token.json")
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data["name"]
    password = data["password"]
    userid = data["userid"]
    gender = data["gender"]
    userType = data["userType"]

    if userType == "Student":
        semester = data["semester"]
        groupid = data["groupid"]
        # Check if username already exists
        if student_collection.find_one({"userid": userid}):
            return jsonify({"error": "User Id already exists"})
        creds = af.login()
        user_info = af.get_user_info(creds)
        root_folder_id = create_folder.create_shared_folder(
            creds, "Unified_Educational_Platform"
        )
        student_collection.insert_one(
            {
                "userid": userid,
                "password": password,
                "name": name,
                "gender": gender,
                "semester": semester,
                "groupid": groupid,
                "google_acc_username": user_info.get("displayName"),
                "gmail_id": user_info.get("emailAddress"),
                "root_folder_id": root_folder_id,
            }
        )
        return jsonify({"message": "Registration successful"})
    else:
        # Check if username already exists
        if teacher_collection.find_one({"userid": userid}):
            return jsonify({"error": "User Id already exists"})
        # Insert new user into the collection
        user_info = af.get_user_info(af.login())
        root_folder_id = create_folder.create_shared_folder(
            af.login(), "Unified_Educational_Platform"
        )
        teacher_collection.insert_one(
            {
                "userid": userid,
                "password": password,
                "name": name,
                "gender": gender,
                "google_acc_username": user_info.get("displayName"),
                "gmail_id": user_info.get("emailAddress"),
                "root_folder_id": root_folder_id,
            }
        )
        return jsonify({"message": "Registration successful"})


@app.route("/login", methods=["POST"])
def login():
    global global_user_id, global_user_type  # Declare global variables
    data = request.json
    userid = data["userid"]
    password = data["password"]
    loginUserType = data["loginUserType"]
    if loginUserType == "Student":
        # Check if username and password match
        user = student_collection.find_one({"userid": userid, "password": password})
        if user:
            global_user_id = userid
            global_user_type = "Student"
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"error": "Invalid credentials"})
    else:
        # Check if username and password match
        user = teacher_collection.find_one({"userid": userid, "password": password})
        if user:
            global_user_id = userid
            global_user_type = "Teacher"
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"error": "Invalid credentials"})


@app.route("/student/dashboard")
def student_dashboard():
    # Render the student dashboard template
    af.login()
    return render_template(
        "dashboard_student.html",
    )


@app.route("/teacher/dashboard")
def teacher_dashboard():
    # Render the teacher dashboard template
    af.login()
    return render_template("dashboard_teacher.html")


@app.route("/create_course", methods=["POST"])
def create_course():
    data = request.form
    new_course_name = data["course_name"]
    new_course_id = data["course_id"]
    group_id = data["group_id"]
    global global_user_id, global_user_type  # Declare global variables

    course = courses_collection.find_one(
        {
            "course_id": new_course_id,
            "course_name": new_course_name,
            "group_id": group_id,
        }
    )
    if course:
        return jsonify({"status": "Course_already_exists", "course": new_course_name})
    courses_collection.insert_one(
        {
            "course_id": new_course_id,
            "course_name": new_course_name,
            "group_id": group_id,
            "faculty_id": global_user_id,
        }
    )
    teacher_collection.update_one(
        {"userid": global_user_id},
        {
            "$push": {
                "courses_taught": {"course_id": new_course_id, "group_id": group_id}
            }
        },
    )
    groups_collection.update_one(
        {"group_id": group_id}, {"$push": {"courses_available": new_course_id}}
    )
    parent_folder = teacher_collection.find_one(
        {"userid": global_user_id}, {"root_folder_id": 1}
    )
    parent_folder_id = parent_folder["root_folder_id"]
    course_folder_id = create_folder.create_shared_folder(
        creds=af.login(), folder_name=new_course_id, parent_folder_id=parent_folder_id
    )
    if folders_collection.find_one({"userid": global_user_id}):
        folders_collection.update_one(
            {"userid": global_user_id},
            {
                "$push": {
                    "course_folder_id": {
                        "course_id": new_course_id,
                        "folder_id": course_folder_id,
                    }
                }
            },
        )
    else:
        folders_collection.insert_one(
            {
                "userid": global_user_id,
                "usertype": global_user_type,
                "course_folder_id": [
                    {
                        "course_id": new_course_id,
                        "folder_id": course_folder_id,
                    }
                ],
            }
        )

    return jsonify({"status": "course_created", "course": new_course_name})


@app.route("/add_course", methods=["POST"])
def addcourse():
    data = request.form
    course_name = data["course_name"]
    course_id = data["course_id"]
    group_id = data["group_id"]
    course = courses_collection.find_one(
        {
            "course_id": course_id,
            "course_name": course_name,
            "group_id": group_id,
        }
    )
    if course:
        student_collection.update_one(
            {"userid": global_user_id},
            {"$push": {"courses": {"course_id": course_id}}},
        )
        parent_folder = student_collection.find_one(
            {"userid": global_user_id}, {"root_folder_id": 1}
        )
        parent_folder_id = parent_folder["root_folder_id"]
        course_folder_id = create_folder.create_shared_folder(
            creds=af.login(), folder_name=course_id, parent_folder_id=parent_folder_id
        )
        # ---------------------------------------
        if folders_collection.find_one({"userid": global_user_id}):
            folders_collection.update_one(
                {"userid": global_user_id},
                {
                    "$push": {
                        "course_folder_id": {
                            "course_id": course_id,
                            "folder_id": course_folder_id,
                        }
                    }
                },
            )
        else:
            folders_collection.insert_one(
                {
                    "userid": global_user_id,
                    "usertype": global_user_type,
                    "course_folder_id": [
                        {
                            "course_id": course_id,
                            "folder_id": course_folder_id,
                        }
                    ],
                }
            )

        # -----------------------
        return jsonify({"status": "course_found", "course": course_name})
    else:
        return jsonify({"status": "course_not_found"})


def get_course_data(user_id):
    courses = courses_collection.find(
        {"faculty_id": user_id},
        {"_id": 0, "course_name": 1, "course_id": 1, "group_id": 1},
    )
    course_list = []
    for course in courses:
        course_list.append(
            courses_collection.find_one({"course_id": course["course_id"]}, {"_id": 0})
        )
    return course_list


@app.route("/data")
def get_data():
    course_data = get_course_data(global_user_id)
    return jsonify(course_data)


def get_student_course_data(user_id):
    courses = student_collection.find_one(
        {"userid": user_id},
        {"_id": 0},
    )
    course_list = []
    if courses.get("courses") == None:
        return course_list
    for course in courses["courses"]:
        course_list.append(
            courses_collection.find_one({"course_id": course["course_id"]}, {"_id": 0})
        )
    return course_list


@app.route("/studentCourseData")
def get_student_data():
    course_data = get_student_course_data(global_user_id)
    return jsonify(course_data)


course_id = None
group_id = None


@app.route("/course_files", methods=["POST"])
def course_files():
    data = request.json
    global course_id, group_id
    course_id = data.get("course_id")
    group_id = data.get("group_id")
    results = aggregrate_v2.get_study_materials(group_id, course_id)
    return jsonify(results)


@app.route("/upload", methods=["POST"])
def upload_file():
    if course_id:
        folder_ids = folders_collection.find_one(
            {"userid": global_user_id, "course_folder_id.course_id": course_id},
            {"_id": 0, "course_folder_id": 1},
        )
        # print(folder_id)
        for i in folder_ids["course_folder_id"]:
            if i["course_id"] == course_id:
                # print(i["folder_id"])
                folder_id = i["folder_id"]
                break
        # print(folder_id)
        file_id = af.upload(af.login(), folder_id)
        uploaded_file = af.get_file_name(af.login(), file_id)
        return jsonify({"file_name": uploaded_file}), 200
    else:
        return jsonify({"file_name": "course not selected"}), 200


if __name__ == "__main__":
    app.run()
