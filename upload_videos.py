import os
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import pandas as pd
from datetime import datetime
import time
import keyboard  # Detect key press

# Define constants for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = "client_secrets.json"  # Path to your client secrets file
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def authenticate_youtube():
    """Authenticate and return the YouTube API client."""
    creds = None
    if os.path.exists("token.json"):
        creds, _ = google.auth.load_credentials_from_file("token.json")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Optionally, save the credentials for future use:
        # with open("token.json", "w") as token:
        #     token.write(creds.to_json())
    
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
    return youtube

def upload_video(youtube, video_file, title, description, scheduled_time):
    """Upload a video to YouTube and schedule it."""
    try:
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {
                "privacyStatus": "private",  # Video remains private until the scheduled time
                "publishAt": scheduled_time,  # Video will go public at the scheduled time
                "selfDeclaredMadeForKids": False
            }
        }

        media_file = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        upload_request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        )

        upload_request.execute()
        print(f"✅ Video '{title}' uploaded and scheduled for {scheduled_time}")
    
    except HttpError as e:
        print(f"❌ An error occurred while uploading '{title}': {e}")

def main():
    # Check if the CSV file exists
    if not os.path.exists("videos.csv"):
        print("❌ Error: videos.csv file not found!")
        return

    # Read the CSV file using comma as delimiter,
    # forcing scheduled_date and schedule_time to be read as strings.
    schedule_df = pd.read_csv("videos.csv", encoding="utf-8-sig", dtype={"scheduled_date": str, "schedule_time": str}).fillna("")
    
    # Clean header names (remove extra spaces)
    schedule_df.columns = schedule_df.columns.str.strip()
    
    # Remove rows that are completely empty
    schedule_df = schedule_df.dropna(how='all')

    # Debug: Print only the first few rows to check the CSV structure.
    print("Debug - CSV Data (first 5 rows):")
    print(schedule_df.head())

    youtube = authenticate_youtube()
    
    for index, row in schedule_df.iterrows():
        # Retrieve and clean the video file path
        video_file = str(row.get("video_file", "")).strip()
        if not video_file:
            print(f"⚠️ Skipping row {index} due to missing video file")
            continue

        # Retrieve title and provide a default if missing
        title = str(row.get("title", "Untitled Video")).strip() or "Untitled Video"
        # Retrieve description (defaults to empty string if missing)
        description = str(row.get("description", "")).strip()

        # Retrieve the scheduled date and time from separate columns.
        scheduled_date = str(row.get("scheduled_date", "")).strip()
        schedule_time_part = str(row.get("schedule_time", "")).strip()

        if not scheduled_date or not schedule_time_part:
            print(f"⚠️ Skipping row {index} due to missing scheduled date or time for video '{title}'")
            continue

        # Combine the date and time strings.
        datetime_str = f"{scheduled_date} {schedule_time_part}"
        dt_obj = None
        # Try different datetime formats.
        for fmt in ("%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M:%S", "%m-%d-%y %H:%M:%S"):
            try:
                dt_obj = datetime.strptime(datetime_str, fmt)
                break
            except ValueError:
                continue

        if not dt_obj:
            print(f"❌ Error parsing datetime for '{title}' (input was '{datetime_str}')")
            continue

        # Convert to ISO 8601 format with a trailing 'Z' (UTC)
        scheduled_iso = dt_obj.isoformat() + "Z"

        # Check if the video file exists
        if not os.path.exists(video_file):
            print(f"❌ Error: Video file '{video_file}' not found! Skipping video '{title}'")
            continue

        # Upload the video
        upload_video(youtube, video_file, title, description, scheduled_iso)
        
        # Check if 'Ctrl+C' was pressed to stop the script
        if keyboard.is_pressed('ctrl+c'):
            print("🚫 Script stopped by user.")
            break
        
        # Small delay to avoid rate limit issues
        time.sleep(5)

if __name__ == "__main__":
    main()
