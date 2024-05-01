from googleapiclient.discovery import build


def create_folder(creds, folder_name, parent_folder_id=None):
    # Authenticate using credentials
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_folder_id:
        file_metadata["parents"] = [parent_folder_id]

    folder = service.files().create(body=file_metadata, fields="id").execute()
    # print("Folder ID: {}".format(folder.get("id")))

    return folder.get("id")


def set_folder_permissions(creds, folder_id, permissions):
    # Authenticate using credentials
    service = build("drive", "v3", credentials=creds)
    for permission in permissions:
        service.permissions().create(
            fileId=folder_id, body=permission, fields="id"
        ).execute()


def create_shared_folder(creds, folder_name, parent_folder_id=None):
    folder_id = create_folder(creds, folder_name, parent_folder_id)
    permissions = [
        {
            "type": "user",
            "role": "writer",
            "emailAddress": "uep-resource@void-uep.iam.gserviceaccount.com",
        }
    ]
    # Specify the permissions for the shared folder
    set_folder_permissions(creds, folder_id, permissions)

    return folder_id
