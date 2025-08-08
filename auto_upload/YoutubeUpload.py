import os
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from content_generator.OpenAI import OpenAI


class YoutubeUpload:

    def __init__(self):
        # Constants
        load_dotenv()
        self.SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
        self.CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT")
        self.CREDENTIALS_FILE = os.getenv("YOUTUBE_TOKEN")


    def get_authenticated_service(self):
        creds = None

        # Correct way to load OAuth2 credentials from token.json
        if os.path.exists(self.CREDENTIALS_FILE):
            creds = Credentials.from_authorized_user_file(self.CREDENTIALS_FILE, self.SCOPES)

        # If no valid credentials, go through OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for next run
            with open(self.CREDENTIALS_FILE, 'w') as token:
                token.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)

    def upload_video(self,file_path, title, description, tags, category_id="25", privacy_status="public"):
        youtube = self.get_authenticated_service()

        # Get tomorrow's date at 8 AM UTC
        tomorrow_8am = datetime.now(timezone.utc).replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)

        # Convert to ISO 8601 string with Z (for UTC)
        publish_at = tomorrow_8am.isoformat().replace("+00:00", "Z")

        body = dict(
            snippet=dict(
                title=title,
                description=description,
                tags=tags,
                categoryId=category_id
            ),
            status=dict(
                privacyStatus="private",  # Required for scheduled publish
                publishAt=publish_at,  # ✅ This is now a string
                selfDeclaredMadeForKids=False
            )
        )

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/*")

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        print(response)
        print("Upload complete.")
        print("Video ID:", response.get("id"))


    def generate_upload(self,article_body,article_title,generated_video):
        youtube_info = OpenAI().youtube_info(article_body)

        self.upload_video(
            file_path=generated_video,
            title=article_title,
            description=youtube_info["description"],
            tags=youtube_info["tags"],
            privacy_status="private"  # public | unlisted | private
        )
