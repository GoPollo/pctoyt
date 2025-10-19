from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Scopes required for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def youtube_authenticate():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

def upload_video(file_path, title, description, category_id="22", keywords=""):
    youtube = youtube_authenticate()
    
    request_body = {
        "snippet": {
            "categoryId": category_id,
            "title": title,
            "description": description,
            "tags": keywords.split(",") if keywords else []
        },
        "status": {
            "privacyStatus": "public"  # or "private" or "unlisted"
        }
    }

    media_file = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    upload_request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = None
    while response is None:
        status, response = upload_request.next_chunk()
        if status:
            print(f"Uploading... {int(status.progress() * 100)}%")
    print("Upload complete!")
    print(f"Video ID: {response['id']}")

# Example usage
upload_video(
    file_path="example.mp4",
    title="My API Uploaded Video",
    description="This video was uploaded using the YouTube Data API!",
    keywords="api,python,youtube"
)
