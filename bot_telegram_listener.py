import os
import sys
import time
import json
import re
import requests
from instagram_tracker import download_instagram_video, send_video_to_telegram, load_config

INSTA_REGEX = re.compile(r"https?://(?:www\.)?instagram\.com/(?:p|reel)/([A-Za-z0-9_-]+)/?")

def listen_and_serve():
    cfg = load_config()
    token = cfg.get("bot_token")
    if not token:
        print("❌ Bot token missing.")
        return

    print("🤖 Instagram Video Downloader Bot Service Active...")
    offset = 0

    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout=20"
            res = requests.get(url, timeout=30)
            data = res.json()

            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    msg = update.get("message")
                    if not msg:
                        continue

                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")

                    # Check for Instagram URL
                    match = INSTA_REGEX.search(text)
                    if match:
                        post_url = match.group(0)
                        print(f"📥 Received Instagram URL from user: {post_url}")
                        
                        # Notify user that download started
                        requests.post(
                            f"https://api.telegram.org/bot{token}/sendMessage",
                            json={
                                "chat_id": chat_id,
                                "text": "⏳ *वीडियो डाउनलोड हो रही है...* कृपया कुछ सेकंड इंतज़ार करें!",
                                "parse_mode": "Markdown"
                            }
                        )

                        # Download video
                        video_path = download_instagram_video(post_url)
                        if video_path and os.path.exists(video_path):
                            caption = (
                                f"🎬 *Instagram Video Ready!*\n\n"
                                f"🔗 {post_url}\n\n"
                                f"✅ *HD वीडियो फाइल डाउनलोड हो गई है!*"
                            )
                            send_video_to_telegram(video_path, caption, token=token, chat_id=chat_id)
                            # Clean up
                            try:
                                os.remove(video_path)
                            except Exception:
                                pass
                        else:
                            requests.post(
                                f"https://api.telegram.org/bot{token}/sendMessage",
                                json={
                                    "chat_id": chat_id,
                                    "text": "❌ वीडियो डाउनलोड नहीं हो सकी। कृपया चेक करें कि पोस्ट पब्लिक है या नहीं।"
                                }
                            )

            time.sleep(1)
        except Exception as e:
            print(f"Polling loop exception: {e}")
            time.sleep(3)

if __name__ == "__main__":
    listen_and_serve()
