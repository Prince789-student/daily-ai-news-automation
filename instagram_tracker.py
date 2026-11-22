import os
import sys
import json
import time
import subprocess
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "instagram_downloads")
SEEN_FILE = os.path.join(BASE_DIR, "seen_instagram_posts.json")
CONFIG_FILE = os.path.join(BASE_DIR, "telegram_config.json")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

TARGET_ACCOUNTS = [
    "https://www.instagram.com/tech.vision24/",
    "https://www.instagram.com/ai.with.etqad/",
    "https://www.instagram.com/inder.code/",
    "https://www.instagram.com/jaihind99232/"
]

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()

def save_seen(seen_set):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen_set)[-1000:], f, indent=2)

def download_instagram_video(url):
    print(f"📥 Downloading Instagram video: {url}")
    out_template = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    cmd = [
        "yt-dlp",
        url,
        "-o", out_template,
        "--no-warnings",
        "--format", "mp4/bestvideo+bestaudio/best"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        # Find newest mp4 file in download directory
        mp4_files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp4")]
        if mp4_files:
            mp4_files.sort(key=os.path.getmtime, reverse=True)
            return mp4_files[0]
    except Exception as e:
        print(f"❌ Download error for {url}: {e}")
    return None

def send_video_to_telegram(video_path, caption, token=None, chat_id=None):
    cfg = load_config()
    bot_token = token or cfg.get("bot_token")
    target_chat = chat_id or cfg.get("chat_id")

    if not bot_token or not target_chat:
        print("❌ Telegram config missing.")
        return False

    print(f"📤 Uploading video ({os.path.getsize(video_path) // 1024} KB) to Telegram...")
    try:
        with open(video_path, "rb") as f:
            res = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendVideo",
                data={
                    "chat_id": target_chat,
                    "caption": caption,
                    "parse_mode": "Markdown"
                },
                files={"video": f},
                timeout=120
            )
            data = res.json()
            if data.get("ok"):
                print("✅ Video delivered successfully to Telegram!")
                return True
            else:
                print(f"⚠️ Telegram sendVideo error: {data}")
    except Exception as e:
        print(f"❌ Failed to send video: {e}")
    return False

def process_url(url, channel_name="Instagram"):
    seen = load_seen()
    clean_url = url.split("?")[0].rstrip("/")
    post_id = clean_url.split("/")[-1]

    if post_id in seen or clean_url in seen:
        print(f"ℹ️ Already processed: {clean_url}")
        return False

    video_path = download_instagram_video(clean_url)
    if video_path and os.path.exists(video_path):
        caption = (
            f"🎬 *New Informational Video Alert!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 *Source:* {channel_name}\n"
            f"🔗 *Post:* {clean_url}\n\n"
            f"✅ *ओरिजिनल HD वीडियो फाइल डाउनलोड करके भेजी गई है!*"
        )
        success = send_video_to_telegram(video_path, caption)
        if success:
            seen.add(post_id)
            seen.add(clean_url)
            save_seen(seen)
            return True
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        process_url(target_url)
    else:
        print("Usage: python instagram_tracker.py <instagram_post_or_reel_url>")
