import os
import sys
import json
import time
import datetime
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from send_telegram import send_telegram_message

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEEN_FILE = os.path.join(BASE_DIR, "seen_leader_posts.json")

LEADERS = [
    {
        "name": "Elon Musk",
        "role": "CEO @ Tesla, xAI, SpaceX, X",
        "emoji": "🚀",
        "query": '"Elon Musk" (tweet OR "posted on X" OR announced OR x.com) when:1d'
    },
    {
        "name": "Mark Zuckerberg",
        "role": "CEO @ Meta (Llama, Threads, Quest)",
        "emoji": "👓",
        "query": '"Mark Zuckerberg" (announced OR "posted on Threads" OR Instagram OR Meta) when:1d'
    },
    {
        "name": "Sam Altman",
        "role": "CEO @ OpenAI (ChatGPT, o-series, GPT)",
        "emoji": "🤖",
        "query": '"Sam Altman" (announced OR "posted on X" OR OpenAI OR tweet) when:1d'
    },
    {
        "name": "Demis Hassabis / Sundar Pichai",
        "role": "Leaders @ Google & DeepMind (Gemini)",
        "emoji": "💎",
        "query": '("Demis Hassabis" OR "Sundar Pichai") (announced OR "posted" OR Gemini OR DeepMind) when:1d'
    },
    {
        "name": "Jensen Huang",
        "role": "CEO @ NVIDIA (AI Chips & Robotics)",
        "emoji": "⚡",
        "query": '"Jensen Huang" (announced OR keynote OR NVIDIA OR chips) when:1d'
    },
    {
        "name": "Andrej Karpathy / Yann LeCun",
        "role": "Top AI Scientists & Pioneers",
        "emoji": "🧠",
        "query": '("Andrej Karpathy" OR "Yann LeCun") (tweet OR "posted" OR AI OR LLM) when:1d'
    }
]

def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()

def save_seen(seen_set):
    # Keep last 500 items
    list_items = list(seen_set)[-500:]
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list_items, f, indent=2, ensure_ascii=False)

def check_leader_updates(send_alerts=True):
    seen = load_seen()
    now_str = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    new_alerts = []

    print(f"[{now_str}] Checking live feeds for Tech Leaders (Musk, Zuck, Altman, etc.)...")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for leader in LEADERS:
        name = leader["name"]
        role = leader["role"]
        emoji = leader["emoji"]
        query = leader["query"]

        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                root = ET.fromstring(resp.read())
                items = root.findall(".//item")[:2]
                
                for item in items:
                    title = item.findtext("title", "").strip()
                    link = item.findtext("link", "").strip()
                    guid = item.findtext("guid", title)

                    if guid in seen or title in seen:
                        continue

                    # Mark as seen
                    seen.add(guid)
                    seen.add(title)

                    clean_title = title
                    source = "Official Wire / X"
                    if " - " in title:
                        clean_title, source = title.rsplit(" - ", 1)

                    # Build high-impact alert
                    alert_msg = (
                        f"🚨 *BREAKING TECH LEADER UPDATE* 🚨\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"{emoji} *व्यक्ति:* *{name}*\n"
                        f"💼 *Role:* _{role}_\n"
                        f"⏰ *समय:* {now_str}\n\n"
                        f"📢 *ताज़ा पोस्ट / घोषणा:*\n"
                        f"\"{clean_title}\"\n\n"
                        f"💡 *सार & महत्व:* {name} द्वारा हालिया शेयर की गई यह महत्वपूर्ण टेक और बिज़नेस अपडेट है।\n\n"
                        f"🔗 [ओरिजिनल पोस्ट / रिपोर्ट देखें]({link}) (Source: {source})\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"⚡ *Instant Alert via Prince News Bot*"
                    )

                    new_alerts.append(alert_msg)

                    if send_alerts:
                        print(f"🔔 Sending alert for {name}: {clean_title[:50]}...")
                        send_telegram_message(alert_msg)
                        time.sleep(1.5)

            # Sleep between leader requests to avoid 429
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Warning checking {name}: {e}")

    save_seen(seen)
    print(f"Done. {len(new_alerts)} new leader updates processed.")
    return new_alerts

if __name__ == "__main__":
    check_leader_updates(send_alerts=True)
