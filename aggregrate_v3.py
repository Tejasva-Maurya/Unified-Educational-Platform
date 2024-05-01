from google.oauth2 import service_account
from googleapiclient.discovery import build


# Google Drive API setup
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "void-uep",
    "private_key_id": "2a7f93c91d4a850244cce5bb1792e4decf6f986d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCw88X/0en9sLEd\npS15pFJJpzGR/GaHwVfH3zY9o73pmdmhB43thvuiByLMLf8AXdEdb2QhS5va3CDK\nk6toufTmNL+GE9ddHFLaHQJAqsQOBQTyvbNG0pJwUxzksdSrKd6BpC0SZYzht2/k\nhcMocq4r8Ge2IsfIxz/9/gvA4KzkwhtWzrRVCKHSU8jcp5xzCpCprZQ6YbuFm4LM\nAivhmiqNTy+EU6P1Zc4GSYm+P9omEvessEYRs2wx9+LdnTzoG9FTYki4fxaQOFi0\nA46IUIMZbt568xaNl/ayckbDu9csxDy0P2bVuvkF1Sbg4N8ccIBEaCwUPpQn4lEj\nk4fcH/ONAgMBAAECggEAI9bDt+vyieSzAq+VNclftzYrNoeZ1o4EsuEVEcfrq3fz\nGYe3qa+IoIj0dcktGAxoUZ9hdtLi9qFV7OGaumPLY6K0VboICP43E6EDd0h+294N\nYgKk4Ee+zAwxUmpoCeC5haVUUaEKtx6ZhX3ICJWtjA2tW7jQoOwmHFHLXJ3EtrH5\nIZZRyBJr8va/K3HGZeFx619e6Ts/5hc9uWdkvv7BkwKpaFkmxWFTFqb0QNDs7iGe\nb8TAr5m0mpTV3DVE/KicNdjl9VDWQwMsQLRo1RO7/WZjK+spQNfbWrWq76VoMiou\nm+NOg8Di2vT32E50V07AspdvG6S0YJ8mWm+cTphNKwKBgQDn+loHNCIlaWnruurf\n8eyG9NC6K71R6zcVaMRaDNEdofltS2g2T8mU/wCyjI5dDdrVWqRbBaDcdu77Nx6e\nUAueWWWa8IqD6Ff+70RYl/bj2yT2+t/HpFWtFbtDrQ6xJliDJWDFtNJGW8SwpqIH\nb9PY/WxvUju+17b+Mk9O9PHMAwKBgQDDRrYM8jkUiOCQqqTVbeHM3Gd35+5YUNcg\nwmifjaWZtzBzT603nXM/xQFnsYB3llLL4V7yl03fj84e4GZkT7oqE5trpywT/BA7\n6lLZOBNSP7Lv/XhbV10cf+j2HzksAx2SCeGBRpFgPwvxZVDzH6UNeFXISisGqUDW\nr+yjKv/VLwKBgQDQq1qgcDzm+lPVQGZW2/+vxjibvwyly7fZAkzd0/mndjQwJEyx\nzkO+S0QNWHIXModOtCJz3jQ9HJ8MSyC3t7k7z56eKRHwZegB4qjQKKJlhJNTt4fk\nxeZrs8inr9wvbhbgoZbTQTyFHbdoT/wgRG+EGTKZUJd9q/1n20mL9LoskQKBgHSu\ns+lYczMJ9uV6kbPWTK4UpN7I/2pWI7W3dLyh7unCxHiii2ZH9q2MEiLbtV+/uwmI\nSSu7rRSA4TEh9QzLdvndbWkOIxBt9WVXxtl04FatKUattlUeBs0YwSMP1SGvWuQA\nc3bDq+pOwdwkJhKgPgemd9uONddtGwktZcC52NSRAoGBAI57wf4YjWxhBwa0yaEW\nCVy7+ztow93X3LdhWj0+uZDZaH/A2QVxMf7AlbSNLS46RBDYBzn9KRpZKgfOkpI2\nPgUyUZc1LvffX2kGZy7NCgK6EsH0Tcko3I+jxFY4IyRv4uKsiZeXaKrRZPyRT1UN\nf1xMuRemA9QQkolIeSidFy1k\n-----END PRIVATE KEY-----\n",
    "client_email": "uep-resource@void-uep.iam.gserviceaccount.com",
    "client_id": "101040672027980611572",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/uep-resource%40void-uep.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}


# Connect to Google Drive API using service account credentials
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)


# from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://void050710:Voiduep050710@void-uep.guig8vk.mongodb.net/?retryWrites=true&w=majority"
)
db = client["CREDENTIALS"]
student_collection = db["Students_Cred"]
teacher_collection = db["Teachers_Cred"]
courses_collection = db["Courses"]
groups_collection = db["Groups"]
folders_collection = db["folder_id"]


def getfolderid(groupid, course_id):
    users_list = []
    users = student_collection.find({"groupid": groupid}, {"_id": 0, "userid": 1})
    for user in users:
        users_list.append(user)

    folders_list = []
    for userid in users_list:
        folder_id = folders_collection.find_one(
            {"userid": userid["userid"], "course_folder_id.course_id": course_id},
            {"_id": 0, "course_folder_id": 1},
        )
        if folder_id == None:
            continue
        for i in folder_id["course_folder_id"]:
            if i["course_id"] == course_id:
                folders_list.append(i["folder_id"])
                break
    faculty_list = []
    faculty = courses_collection.find(
        {"group_id": groupid, "course_id": course_id}, {"_id": 0, "faculty_id": 1}
    )
    for i in faculty:
        faculty_list.append(i)
    for facultyid in faculty_list:
        folder_id = folders_collection.find_one(
            {
                "userid": facultyid["faculty_id"],
                "course_folder_id.course_id": course_id,
            },
            {"_id": 0, "course_folder_id": 1},
        )
        if folder_id == None:
            break
        for i in folder_id["course_folder_id"]:
            if i["course_id"] == course_id:
                folders_list.append(i["folder_id"])

    return folders_list


def get_study_materials(group_id, course_id):
    # Retrieve files from users' folders in Google Drive
    folder_ids = getfolderid(groupid=group_id, course_id=course_id)
    materials = []
    for user_folder_id in folder_ids:
        results = (
            drive_service.files().list(q=f"'{user_folder_id}' in parents").execute()
        )
        for file in results.get("files", []):
            materials.append(
                {
                    "name": file["name"],
                    "link": f"https://drive.google.com/file/d/{file['id']}",
                }
            )
    return materials
