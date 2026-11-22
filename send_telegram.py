import os
import sys
import json
import time
import urllib.parse
import urllib.request

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "telegram_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(token, chat_id=None):
    config = load_config()
    config["bot_token"] = token.strip()
    if chat_id:
        config["chat_id"] = str(chat_id).strip()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    return config

def auto_detect_chat_id(bot_token):
    """Auto-detect chat_id from Telegram getUpdates when user clicks Start"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TelegramNewsBot/1.0"})
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode("utf-8"))
            if data.get("ok") and data.get("result"):
                # Get the latest message's chat id
                last_update = data["result"][-1]
                msg = last_update.get("message") or last_update.get("channel_post")
                if msg and "chat" in msg:
                    chat_id = str(msg["chat"]["id"])
                    print(f"✅ Chat ID auto-detected successfully: {chat_id}")
                    save_config(bot_token, chat_id)
                    return chat_id
    except Exception as e:
        print(f"⚠️ Could not auto-detect chat_id: {e}")
    return None

def send_telegram_message(text, token=None, chat_id=None):
    config = load_config()
    bot_token = token or config.get("bot_token") or os.environ.get("TELEGRAM_BOT_TOKEN")
    target_chat = chat_id or config.get("chat_id") or os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token:
        print("❌ [Setup Required] Telegram Bot Token missing hai.")
        return False

    if not target_chat:
        print("🔍 Chat ID detect karne ki koshish kar rahe hain...")
        target_chat = auto_detect_chat_id(bot_token)
        if not target_chat:
            print("⚠️ Kripya apne Telegram Bot ko khol kar 'Start' button dabayein, fir dubara try karein.")
            return False

    # Telegram message length limit is 4096. Split into chunks if needed.
    max_len = 3800
    chunks = []
    if len(text) <= max_len:
        chunks = [text]
    else:
        parts = text.split("\n\n---\n\n")
        current_chunk = []
        current_len = 0
        for part in parts:
            part_len = len(part) + 8
            if current_len + part_len > max_len and current_chunk:
                chunks.append("\n\n---\n\n".join(current_chunk))
                current_chunk = [part]
                current_len = len(part)
            else:
                current_chunk.append(part)
                current_len += part_len
        if current_chunk:
            chunks.append("\n\n---\n\n".join(current_chunk))

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    success_all = True
    for idx, chunk in enumerate(chunks, 1):
        payload = {
            "chat_id": target_chat,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }
        data = json.dumps(payload).encode("utf-8")
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json", "User-Agent": "TelegramNewsBot/1.0"}
            )
            with urllib.request.urlopen(req, timeout=20) as res:
                resp = json.loads(res.read().decode("utf-8"))
                if resp.get("ok"):
                    if len(chunks) > 1:
                        print(f"✅ Telegram message part {idx}/{len(chunks)} sent!")
                        time.sleep(1.2)
                    else:
                        print(f"✅ Telegram par message safaltapoorvak bhej diya gaya! (Chat ID: {target_chat})")
                else:
                    print(f"⚠️ Telegram API error on part {idx}: {resp}")
                    success_all = False
        except Exception as e:
            print(f"❌ Failed to send Telegram message part {idx}: {e}", file=sys.stderr)
            success_all = False

    return success_all

if __name__ == "__main__":
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
        send_telegram_message(msg)
    else:
        print("Usage: python send_telegram.py \"Your Message\"")
