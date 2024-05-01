import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload


import create_folder as cf

# If modifying these scopes, delete the file token.json.


# ----------------------------------utility-------------------------------------------------------------------------


# select folder and return its path
def select_folder():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.attributes("-topmost", True)  # Bring dialog to the front
    root.withdraw()  # Hide the main window
    initial_dir = os.path.expanduser("~/Downloads")  # Path to Downloads folder
    folder_path = filedialog.askdirectory(
        initialdir=initial_dir
    )  # Open file explorer to select folder
    root.destroy()  # Close the tkinter window
    return folder_path


# selected_folder = select_folder()
# print("Selected Folder:", selected_folder)


# select file and return its path
def select_file():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.attributes("-topmost", True)  # Bring dialog to the front
    root.withdraw()  # Hide the main window
    initial_dir = os.path.expanduser("~/Downloads")  # Path to Downloads folder
    file_path = filedialog.askopenfilename(
        initialdir=initial_dir
    )  # Open file explorer to select file
    root.destroy()  # Close the tkinter window
    return file_path


# selected_file = select_file()
# print("Selected File:", selected_file)


# -----------------------------------------------------------------------------------------------------------------------


SCOPES = ["https://www.googleapis.com/auth/drive"]


def login():
    """Fetches user information using the Drive v3 API."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return creds

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            return creds


def get_user_info(creds):
    try:
        service = build("drive", "v3", credentials=creds)
        # Call the Drive v3 API to fetch user information
        about = service.about().get(fields="user").execute()
        user_info = about.get("user")
        if not user_info:
            print("No user information found.")
            return None
        return user_info
    except HttpError as error:
        # TODO: Handle errors from Drive API.
        print(f"An error occurred: {error}")
        return None


def upload(creds, folder_id):
    service = build("drive", "v3", credentials=creds)
    folder_id = folder_id

    # File path of the file to upload
    file_path = select_file()

    # File metadata
    file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}

    # Upload the file
    media = MediaFileUpload(file_path)
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    # print("File ID: %s" % file.get("id"))
    # return f"Uploading file {file["name"]}"
    # print(f"file Uploaded")
    fileid = file.get("id")

    permissions = [
        {
            "type": "user",
            "role": "writer",
            "emailAddress": "uep-resource@void-uep.iam.gserviceaccount.com",
        },
        {"type": "anyone", "role": "reader"},
    ]
    cf.set_folder_permissions(creds=creds, folder_id=fileid, permissions=permissions)
    return fileid


def get_file_name(creds, file_id):

    # Build the service
    service = build("drive", "v3", credentials=creds)

    # Get the file's metadata
    request = service.files().get(fileId=file_id)

    # Send the request and get the response
    response = request.execute()

    # The file's name is stored in the 'name' field of the response
    file_name = response["name"]

    # print(f"File Name: {file_name}")
    return file_name


def download_file(creds, file_id):
    download_folder_path = rf"{select_folder()}"
    service = build("drive", "v3", credentials=creds)

    request = service.files().get_media(fileId=file_id)
    modified_path = f"{download_folder_path}/{get_file_name(creds,file_id)}"

    with io.FileIO(modified_path, mode="wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
    print("Download Complete!")
