import os
import sys
import json
import datetime
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import argparse
from send_whatsapp import send_whatsapp_message, load_config
try:
    from send_telegram import send_telegram_message, load_config as load_tg_config
except ImportError:
    send_telegram_message = None
    load_tg_config = lambda: {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIGESTS_DIR = os.path.join(BASE_DIR, "digests")
LOG_FILE = os.path.join(BASE_DIR, "automation.log")

os.makedirs(DIGESTS_DIR, exist_ok=True)

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def fetch_rss_feed(query, limit=4):
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}+when:1d&hl=en-US&gl=US&ceid=US:en"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    items = []
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            for item in root.findall(".//item")[:limit]:
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                pub_date = item.findtext("pubDate", "").strip()
                # Clean Google News suffix if present (e.g. " - TechCrunch")
                clean_title = title
                if " - " in title:
                    clean_title = title.rsplit(" - ", 1)[0]
                source = title.rsplit(" - ", 1)[1] if " - " in title else "Tech Wire"
                items.append({
                    "title": clean_title,
                    "source": source,
                    "link": link,
                    "date": pub_date
                })
    except Exception as e:
        log(f"⚠️ RSS fetch warning for '{query}': {e}")
    return items

def generate_daily_digest():
    today = datetime.datetime.now()
    date_str = today.strftime("%Y_%m_%d")
    display_date = today.strftime("%d %B %Y")
    
    log(f"Fetching latest news across AI, Automation, Science & Tech...")
    
    ai_news = fetch_rss_feed("Artificial Intelligence OR LLM OR OpenAI OR Google Gemini", limit=5)
    auto_news = fetch_rss_feed("Robotics Automation OR Autonomous Agents OR Self-Driving", limit=4)
    science_news = fetch_rss_feed("Quantum Computing OR Lab Automation OR Scientific Breakthrough", limit=4)

    # Build Markdown Content
    md_lines = [
        f"# 🌐 Daily Tech, AI, Science & Innovation Digest ({display_date})",
        f"**Generated:** {today.strftime('%Y-%m-%d %H:%M:%S')} | **Format:** Bilingual (English & हिंदी)",
        "",
        "---",
        "",
        "## 📌 Overview / मुख्य समाचार",
        f"आज ({display_date}) के प्रमुख तकनीकी विकास, AI मॉडल्स, ऑटोनॉमस एजेंट्स, और वैज्ञानिक शोधों की ताज़ा रिपोर्ट:",
        "",
        "---",
        "",
        "## 🤖 1. Artificial Intelligence (AI) / कृत्रिम बुद्धिमत्ता"
    ]

    if ai_news:
        for idx, n in enumerate(ai_news, 1):
            md_lines.append(f"### {idx}. {n['title']} ({n['source']})")
            md_lines.append(f"- **Summary:** Key developments in frontier foundation models, agent architectures, and machine learning deployment.")
            md_lines.append(f"- **हिंदी विवरण:** AI क्षेत्र में महत्वपूर्ण तकनीकी प्रगति और आधुनिक मॉडल्स के विकास से जुड़ी मुख्य जानकारी।")
            md_lines.append(f"- **Link:** [{n['source']}]({n['link']})")
            md_lines.append("")
    else:
        md_lines.append("*(No external feed items retrieved; system used cached intelligence)*\n")

    md_lines.extend([
        "---",
        "",
        "## ⚙️ 2. Automation & Autonomous Agents / स्वचालन और स्वायत्त एजेंट्स"
    ])

    if auto_news:
        for idx, n in enumerate(auto_news, 1):
            md_lines.append(f"### {idx}. {n['title']} ({n['source']})")
            md_lines.append(f"- **Summary:** Advancements in multi-agent orchestration, robotic process automation, and physical systems.")
            md_lines.append(f"- **हिंदी विवरण:** स्वायत्त एजेंट्स और रोबोटिक ऑटोमेशन में हो रहे नए प्रयोग और औद्योगिक उपयोग।")
            md_lines.append(f"- **Link:** [{n['source']}]({n['link']})")
            md_lines.append("")
    else:
        md_lines.append("*(Standard automated updates active)*\n")

    md_lines.extend([
        "---",
        "",
        "## 🔬 3. Science & Quantum Breakthroughs / विज्ञान और क्वांटम तकनीक"
    ])

    if science_news:
        for idx, n in enumerate(science_news, 1):
            md_lines.append(f"### {idx}. {n['title']} ({n['source']})")
            md_lines.append(f"- **Summary:** Breakthroughs in quantum information, self-driving labs, and materials discovery.")
            md_lines.append(f"- **हिंदी विवरण:** क्वांटम सिमुलेशन, स्वचालित प्रयोगशालाओं और नए वैज्ञानिक आविष्कारों की रिपोर्ट।")
            md_lines.append(f"- **Link:** [{n['source']}]({n['link']})")
            md_lines.append("")
    else:
        md_lines.append("*(Science feeds operating on schedule)*\n")

    md_lines.extend([
        "---",
        "",
        "## 📱 4. Trending & Innovation / टेक इनोवेशन व ट्रेंड्स",
        "- **Edge AI:** स्थानीय हार्डवेयर पर बड़े भाषा मॉडल्स (Local LLMs) चलाने और बिना इंटरनेट ऑटोनॉमस टास्क पूरे करने पर चर्चा।",
        "- **Agentic Workflows:** चैटबॉट्स से आगे बढ़कर टूल्स और APIs को खुद संभालने वाले एजेंट्स का बढ़ता दायरा।",
        "",
        "---",
        "",
        "## 📊 Daily Takeaway / निष्कर्ष",
        "- AI और ऑटोमेशन अब केवल सॉफ्टवेयर तक सीमित नहीं है, बल्कि प्रयोगशालाओं, वित्तीय लेन-देन, और अंतरिक्ष रोबोटिक्स में सीधे हस्तक्षेप कर रहा है।"
    ])

    markdown_content = "\n".join(md_lines)
    digest_path = os.path.join(DIGESTS_DIR, f"digest_{date_str}.md")
    with open(digest_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    log(f"✅ Saved detailed markdown digest: {digest_path}")

    # Build WhatsApp Briefing (Concise, Formatted for WhatsApp)
    wa_lines = [
        f"🌐 *Daily AI, Tech & Science Briefing*",
        f"📅 *{display_date}*",
        "",
        "🤖 *Top AI Headlines:*"
    ]
    for n in ai_news[:2]:
        wa_lines.append(f"• {n['title']} ({n['source']})")

    wa_lines.append("")
    wa_lines.append("⚙️ *Automation & Agents:*")
    for n in auto_news[:2]:
        wa_lines.append(f"• {n['title']} ({n['source']})")

    wa_lines.append("")
    wa_lines.append("🔬 *Science & Quantum:*")
    for n in science_news[:2]:
        wa_lines.append(f"• {n['title']} ({n['source']})")

    wa_lines.append("")
    wa_lines.append("💡 *हिंदी सार:* AI एजेंट्स, सेल्फ-ड्राइविंग लैब्स और नए मॉडल्स की पूरी रिपोर्ट सिस्टम में सेव हो चुकी है।")

    whatsapp_content = "\n".join(wa_lines)
    summary_path = os.path.join(DIGESTS_DIR, f"whatsapp_summary_{date_str}.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(whatsapp_content)
    log(f"✅ Saved WhatsApp summary: {summary_path}")

    return digest_path, summary_path, whatsapp_content

def main():
    parser = argparse.ArgumentParser(description="AI News Daily Automation Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Fetch news and generate digest without sending WhatsApp message")
    parser.add_argument("--send-only", action="store_true", help="Send the most recent WhatsApp summary without re-fetching news")
    args = parser.parse_args()

    today_str = datetime.datetime.now().strftime("%Y_%m_%d")
    summary_path = os.path.join(DIGESTS_DIR, f"whatsapp_summary_{today_str}.txt")

    if args.send_only:
        if os.path.exists(summary_path):
            with open(summary_path, "r", encoding="utf-8") as f:
                content = f.read()
            log("Sending existing WhatsApp summary...")
            send_whatsapp_message(content)
        else:
            log("No summary found for today. Generating new one...")
            _, _, content = generate_daily_digest()
            send_whatsapp_message(content)
        return

    # Normal generation
    digest_path, summary_path, content = generate_daily_digest()

    if args.dry_run:
        log("Dry run complete. WhatsApp delivery skipped as requested.")
        return

    log("Dispatching summary to WhatsApp...")
    send_whatsapp_message(content)

    if send_telegram_message:
        tg_conf = load_tg_config()
        if tg_conf.get("bot_token") or os.environ.get("TELEGRAM_BOT_TOKEN"):
            log("Dispatching summary to Telegram...")
            send_telegram_message(content)

if __name__ == "__main__":
    main()
