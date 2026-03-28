from flask import Flask, render_template
import requests
import boto3
import os
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# ─── CONFIG ───────────────────────────────────────────────
TICKETMASTER_API_KEY = "YOUR_TICKETMASTER_API_KEY"   # Replace with your key
S3_BUCKET_NAME       = "unievents-media-bucket-yourname"  # Replace with your bucket name
AWS_REGION           = "us-east-1"                   # Change if you used a different region
# ──────────────────────────────────────────────────────────

def fetch_events():
    """Fetch events from Ticketmaster API"""
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "size": 12,
        "sort": "date,asc"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        events_raw = data.get("_embedded", {}).get("events", [])
        events = []
        for e in events_raw:
            image_url = e.get("images", [{}])[0].get("url", "")
            s3_url = upload_image_to_s3(image_url, e.get("id", "")) if image_url else ""
            events.append({
                "title":  e.get("name", "No Title"),
                "date":   e.get("dates", {}).get("start", {}).get("localDate", "TBD"),
                "venue":  e.get("_embedded", {}).get("venues", [{}])[0].get("name", "TBD"),
                "city":   e.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name", ""),
                "description": e.get("info", "No description available."),
                "image":  s3_url if s3_url else image_url,
                "url":    e.get("url", "#")
            })
        return events
    except Exception as ex:
        print(f"Error fetching events: {ex}")
        return []


def upload_image_to_s3(image_url, event_id):
    """Download image from URL and upload to S3"""
    try:
        img_data = requests.get(image_url, timeout=10).content
        s3 = boto3.client("s3", region_name=AWS_REGION)
        key = f"event-images/{event_id}.jpg"
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
            Body=img_data,
            ContentType="image/jpeg",
        )
        return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
    except NoCredentialsError:
        print("AWS credentials not found — using original image URL instead")
        return ""
    except Exception as ex:
        print(f"S3 upload error: {ex}")
        return ""


@app.route("/")
def index():
    events = fetch_events()
    return render_template("index.html", events=events)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
