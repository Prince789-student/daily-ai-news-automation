import os
import sys
import json
import time
import re
import subprocess
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "instagram_downloads")
SEEN_FILE = os.path.join(BASE_DIR, "seen_instagram_posts.json")
CONFIG_FILE = os.path.join(BASE_DIR, "telegram_config.json")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Top Indian & Global High-Value AI, Coding & Automation Creators
TARGET_CHANNELS = [
    "codernormie",
    "rachit.speaks",
    "beyondtahir",
    "mister.a1b",
    "_akshay_nandwana",
    "agam.nexgen.ai",
    "vivekrajaniofficial",
    "sunmughan",
    "techtalkswithayush",
    "rise.chapter",
    "priyantan2.0",
    "baljeet.ai",
    "its_anmol.ai",
    "tech.vision24",
    "ai.with.etqad",
    "inder.code",
    "jaihind99232",
    "kaushal.builds",
    "100xdevs",
    "hiteshchoudharyofficial",
    "codewithharry",
    "krishnaik06",
    "vaibhavsisinty",
    "the_ai_revolution",
    "ai_explorerr",
    "creators.ai",
    "codewithsrajan",
    "techno_ruhez",
    "sanidhyatulsinandan",
    "futurepedia_io",
    "techinsider_ai",
    "mattvidproai",
    "digi.aniket",
    "techietarget"
]

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # Cloud environment fallback
    return {
        "bot_token": os.environ.get("TELEGRAM_BOT_TOKEN", "9257539042:AAHZk7ijbvyWbsCydhnoZg5wtg583mce1wk"),
        "chat_id": os.environ.get("TELEGRAM_CHAT_ID", "1762619355")
    }

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
        json.dump(list(seen_set)[-2000:], f, indent=2)

def get_selenium_driver():
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        print(f"⚠️ Selenium init note: {e}")
        return None

def fetch_reels_from_channel(driver, username, limit=3):
    url = f"https://www.instagram.com/{username}/reels/"
    print(f"🔍 Checking channel: @{username} ...")
    try:
        driver.get(url)
        time.sleep(3.5)
        html = driver.page_source
        reels = re.findall(r'/(?:reel|p)/([A-Za-z0-9_-]{8,})', html)
        unique_reels = list(dict.fromkeys(reels))
        print(f"  👉 Found {len(unique_reels)} reels for @{username}")
        return unique_reels[:limit]
    except Exception as e:
        print(f"  ❌ Error fetching @{username}: {e}")
        return []

def extract_metadata_and_download(url, post_id):
    out_path = os.path.join(DOWNLOAD_DIR, f"{post_id}.mp4")
    if os.path.exists(out_path):
        try:
            os.remove(out_path)
        except Exception:
            pass

    cmd_meta = ["yt-dlp", "--dump-json", "--no-warnings", url]
    metadata = {}
    try:
        res = subprocess.run(cmd_meta, capture_output=True, text=True, timeout=35)
        if res.stdout:
            metadata = json.loads(res.stdout)
    except Exception as e:
        print(f"  Metadata note: {e}")

    cmd_dl = [
        "yt-dlp",
        url,
        "-o", out_path,
        "--no-warnings",
        "--format", "mp4/bestvideo+bestaudio/best"
    ]
    try:
        subprocess.run(cmd_dl, capture_output=True, text=True, timeout=90)
    except Exception as e:
        print(f"  Download error: {e}")

    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        return out_path, metadata
    return None, metadata

def decode_secret_tools(desc):
    if not desc:
        return ""

    urls = re.findall(r"https?://[^\s)\]]+", desc)
    github_links = [u for u in urls if "github.com" in u]
    other_links = [u for u in urls if "github.com" not in u and "instagram.com" not in u]

    # Check for "Comment XYZ" patterns
    comment_prompt = re.findall(r'Comment [“"\'\‘]([A-Za-z0-9_-]+)[”"\'\’]', desc, re.IGNORECASE)
    prompt_word = comment_prompt[0] if comment_prompt else None

    # Known repository mapping for popular AI alternatives
    tool_map = {
        "affine": ("AFFiNE (Notion Alternative)", "https://github.com/toeverything/AFFiNE"),
        "cap": ("Cap (Loom Alternative)", "https://github.com/CapSoftware/Cap"),
        "cal": ("Cal.com (Calendly Alternative)", "https://github.com/calcom/cal.com"),
        "chatwoot": ("Chatwoot (Intercom Alternative)", "https://github.com/chatwoot/chatwoot"),
        "openproject": ("OpenProject (Asana Alternative)", "https://github.com/opf/openproject"),
        "f5-tts": ("F5-TTS (ElevenLabs Alternative)", "https://github.com/SWivid/F5-TTS"),
        "whisper": ("Whisper.cpp (Speech-to-Text)", "https://github.com/ggerganov/whisper.cpp"),
        "cogvideo": ("CogVideoX (AI Video Model)", "https://github.com/THUDM/CogVideo"),
        "wan": ("Wan2.1 (Open Video Generation)", "https://github.com/Wan-Video/Wan2.1"),
        "opus": ("OpusClip AI", "https://www.opus.pro/"),
        "vyro": ("Vyro Creator Platform", "https://vyro.ai/"),
        "twenty": ("Twenty (Salesforce Alternative)", "https://github.com/twentyhq/twenty"),
        "sellbird": ("Sellbird AI Leads", "https://github.com/ethanplusai/sellbird")
    }

    detected_tools = []
    desc_lower = desc.lower()
    for key, (name, link) in tool_map.items():
        if key in desc_lower and link not in github_links and link not in other_links:
            detected_tools.append(f"• 🛠️ {name}: {link}")

    lines = []
    if prompt_word:
        lines.append(f"💡 Creator Prompts: 'Comment {prompt_word} for links' (Decoded automatically!)")

    if github_links:
        for g in github_links[:3]:
            lines.append(f"• 🔗 GitHub: {g}")
    if other_links:
        for o in other_links[:3]:
            lines.append(f"• 🌐 Official Website: {o}")
    if detected_tools:
        lines.extend(detected_tools[:4])

    if not lines:
        lines.append("• 🛠️ Video Tools: इस वीडियो में बताए गए टूल्स और ओपन-सोर्स कोड वीडियो के अंदर दिखाए गए हैं।")

    return "\n".join(lines)

def send_video_to_telegram(video_path, caption, cfg):
    bot_token = cfg.get("bot_token")
    chat_id = cfg.get("chat_id")

    if not bot_token or not chat_id:
        print("❌ Telegram credentials missing.")
        return False

    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"📤 Uploading video ({size_mb:.2f} MB) to Telegram...")

    # Telegram caption character limit is 1024
    if len(caption) > 1000:
        short_caption = caption[:950] + "...\n(सारे लिंक्स नीचे अगले मैसेज में हैं 👇)"
        followup_text = caption
    else:
        short_caption = caption
        followup_text = None

    try:
        with open(video_path, "rb") as vf:
            res = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendVideo",
                data={
                    "chat_id": chat_id,
                    "caption": short_caption
                },
                files={"video": vf},
                timeout=180
            )
            data = res.json()
            if data.get("ok"):
                print("  ✅ Video delivered successfully to Telegram!")
                if followup_text:
                    time.sleep(1)
                    requests.post(
                        f"https://api.telegram.org/bot{bot_token}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": followup_text,
                            "disable_web_page_preview": True
                        },
                        timeout=30
                    )
                return True
            else:
                print(f"  ⚠️ sendVideo error: {data}")
    except Exception as e:
        print(f"  ❌ Upload exception: {e}")
    return False

def process_single_reel(reel_url_or_id, channel_hint="Instagram Creator"):
    cfg = load_config()
    seen = load_seen()

    clean_id = reel_url_or_id.split("?")[0].rstrip("/").split("/")[-1]
    if clean_id in seen:
        print(f"ℹ️ Already processed: {clean_id}")
        return True

    full_url = f"https://www.instagram.com/reel/{clean_id}/"
    video_path, metadata = extract_metadata_and_download(full_url, clean_id)

    if not video_path:
        print(f"❌ Failed to download {full_url}")
        return False

    channel = metadata.get("channel") or channel_hint
    desc = metadata.get("description", "")
    short_title = desc.split("\n")[0][:120] if desc else "Tech & AI Video"
    tools_block = decode_secret_tools(desc)

    caption = (
        f"🎬 New Reel: @{channel}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 विषय: {short_title}\n\n"
        f"🔓 Unlocked Secret Tools & Repos:\n"
        f"{tools_block}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 Original Reel: {full_url}\n"
        f"💡 बिना कमेंट किए वीडियो और टूल्स सीधे आपके टेलीग्राम पर!"
    )

    success = send_video_to_telegram(video_path, caption, cfg)
    if success:
        seen.add(clean_id)
        save_seen(seen)
        # Clean up local file after send
        try:
            os.remove(video_path)
        except Exception:
            pass
        return True
    return False

def run_channel_monitor():
    print("🚀 Starting Instagram Tech & AI Cloud Monitor...")
    cfg = load_config()
    seen = load_seen()
    driver = get_selenium_driver()

    if not driver:
        print("❌ Selenium driver unavailable, skipping sweep.")
        return

    delivered_count = 0
    try:
        for channel in TARGET_CHANNELS:
            reels = fetch_reels_from_channel(driver, channel, limit=2)
            for r_id in reels:
                if r_id not in seen:
                    print(f"✨ New unseen reel found: {r_id} from @{channel}!")
                    ok = process_single_reel(r_id, channel_hint=channel)
                    if ok:
                        delivered_count += 1
                        time.sleep(2)
    finally:
        driver.quit()

    print(f"🏁 Instagram Sweep Complete. Delivered {delivered_count} new reels.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        process_single_reel(arg)
    else:
        run_channel_monitor()
