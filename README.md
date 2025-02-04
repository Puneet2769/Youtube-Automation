# 🎥 YouTube Automation & Scheduling Tool

## 📌 Project Overview
This project is designed to **automate your YouTube uploads**. It not only uploads your videos (or even YouTube Shorts) but also **schedules them to go live** at your specified date and time! With this tool, you can provide essential video metadata—such as title, description, and more—via a CSV file, and let the script handle authentication, scheduling, and uploading using the **YouTube Data API v3**.

---

## 🔧 Prerequisites

Before you get started, make sure you have:

- **Python 3** installed on your system.
- All required dependencies installed (see below).
- A **Google Cloud Project** with the YouTube Data API enabled.
- An OAuth `client_secrets.json` file for API authentication.

---

## 🚀 Setup Guide

### 1️⃣ Google API Credentials
1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **YouTube Data API v3**.
3. Navigate to **APIs & Services > Credentials** and create an **OAuth Client ID**.
4. Download the `client_secrets.json` file and place it in your working directory.

### 2️⃣ Install Dependencies
Install all required libraries using pip:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas keyboard
```

### 3️⃣ CSV File Setup (`videos.csv`)
Create a CSV file named `videos.csv` in your working directory. This file should contain the details of each video you want to upload and schedule. Here is the expected format:

| video_file  | title           | description          | scheduled_date | schedule_time |
|-------------|-----------------|----------------------|----------------|---------------|
| video1.mp4  | My First Video  | This is a test video | 2025-02-10     | 14:30:00      |
| video2.mp4  | Second Upload   | Another test video   | 2025-02-12     | 16:00:00      |

- **video_file**: Path to your video file (must exist in your working directory).
- **title**: The title of the video.
- **description**: The video description.
- **scheduled_date**: The date when the video should be published (`YYYY-MM-DD`).
- **schedule_time**: The time when the video should be published (`HH:MM:SS`).

*Example CSV row:*
```csv
video1.mp4,My First Video,This is a test video,2025-02-10,14:30:00
```

### 4️⃣ Running the Script
Make sure that all required files (`client_secrets.json`, `videos.csv`, and your video files) are in your working directory. Then, simply run:
```bash
python upload_videos.py
```

---

## 🛠 How It Works

1. **Authentication:**  
   The script authenticates with YouTube using OAuth. On the first run, a browser window will open to complete the authentication process. A `token.json` is generated and used for subsequent runs.

2. **CSV Processing:**  
   The script reads `videos.csv` to gather video file paths, titles, descriptions, and scheduled dates/times.  
   ➡️ *This allows you to schedule multiple uploads at once!*

3. **Scheduling & Uploading:**  
   Each video is uploaded as **private** and scheduled to be published at the specified time. Whether it's a regular video or a YouTube Short, the scheduled metadata (title, description, etc.) is applied.

4. **Automation:**  
   After processing each CSV row, the script waits a few seconds to avoid rate limits. You can stop the script anytime by pressing **Ctrl+C**.

---

## ❗ Important Notes

- **File Locations:**  
  All files—`client_secrets.json`, `videos.csv`, and your video files—must be in the same working directory as the script.

- **Scheduling Accuracy:**  
  Ensure that the `scheduled_date` and `schedule_time` in the CSV are in the correct format to avoid errors during scheduling.

- **Stopping the Process:**  
  If you need to halt the uploads, simply press **Ctrl+C** while the script is running.

---

## 🎬 Final Thoughts
This tool streamlines the process of uploading and scheduling YouTube content, making it a perfect solution for content creators who want to manage their uploads efficiently. Enjoy hassle-free automation and get back to creating amazing content! 🚀📹

---

## 🙌 Credits
Created by **Puneet Poddar**

---
