from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

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


@app.route("/")
def index():
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
        # Check if username already exists
        if student_collection.find_one({"userid": userid}):
            return jsonify({"error": "User Id already exists"})
        student_collection.insert_one(
            {
                "name": name,
                "gender": gender,
                "userid": userid,
                "password": password,
                "semester": semester,
            }
        )
        return jsonify({"message": "Registration successful"})
    else:
        # Check if username already exists
        if teacher_collection.find_one({"userid": userid}):
            return jsonify({"error": "User Id already exists"})
        # Insert new user into the collection
        teacher_collection.insert_one(
            {"userid": userid, "password": password, "name": name, "gender": gender}
        )
        return jsonify({"message": "Registration successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    userid = data["userid"]
    password = data["password"]
    loginUserType = data["loginUserType"]
    if loginUserType == "Student":
        # Check if username and password match
        user = student_collection.find_one({"userid": userid, "password": password})
        if user:
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"error": "Invalid credentials"})
    else:
        # Check if username and password match
        user = teacher_collection.find_one({"userid": userid, "password": password})
        if user:
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"error": "Invalid credentials"})


@app.route("/student/dashboard")
def student_dashboard():
    # Render the student dashboard template
    return render_template("student_dashboard.html")


@app.route("/teacher/dashboard")
def teacher_dashboard():
    # Render the teacher dashboard template
    return render_template("teacher_dashboard.html")


SERVICE_ACCOUNT_FILE = "cred-1.json"
DRIVE_FOLDER_ID = "1t1JPBSTwxTywzXwAltXghn0g3oPPR2-R"

# Create a Google Drive service instance
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE
)
drive_service = build("drive", "v3", credentials=credentials)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    file_metadata = {"name": file.filename, "parents": [DRIVE_FOLDER_ID]}

    # Read the file content
    file_content = file.read()

    # Create a BytesIO object to pass the file content
    media = MediaIoBaseUpload(
        BytesIO(file_content), mimetype=file.mimetype, resumable=True
    )

    # Upload the file to Google Drive
    uploaded_file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    return jsonify({"file_id": uploaded_file.get("id")}), 200


if __name__ == "__main__":
    app.run(debug=True)
