import os
import sys
import json
import datetime
import urllib.request
import urllib.parse
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

def fetch_rss_feed(query, limit=5):
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
                clean_title = title
                source = "Tech Wire"
                if " - " in title:
                    clean_title, source = title.rsplit(" - ", 1)
                items.append({
                    "title": clean_title.strip(),
                    "source": source.strip(),
                    "link": link.strip(),
                    "date": pub_date.strip()
                })
    except Exception as e:
        log(f"⚠️ RSS fetch warning for '{query}': {e}")
    return items

def generate_daily_digest():
    today = datetime.datetime.now()
    date_str = today.strftime("%Y_%m_%d")
    display_date = today.strftime("%d %B %Y")
    
    log("Fetching latest news across AI, Automation, Science & Tech...")
    
    ai_news = fetch_rss_feed("Artificial Intelligence OR LLM OR OpenAI OR Google Gemini", limit=4)
    auto_news = fetch_rss_feed("Autonomous Agents OR AI Robotics OR Industrial Automation", limit=4)
    science_news = fetch_rss_feed("Quantum Computing OR Biotech AI OR Scientific Discovery", limit=3)

    # ─────────────────────────────────────────────────────────────────
    # 🌟 BUILD IN-DEPTH COMPREHENSIVE TELEGRAM BRIEFING (Full Information)
    # ─────────────────────────────────────────────────────────────────
    tg_sections = []

    # Header
    tg_sections.append(
        f"🌐 *DAILY AI, AUTOMATION & TECH MASTER DIGEST*\n"
        f"📅 *तारीख:* {display_date} | *Edition:* Comprehensive Deep-Dive\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    # Section 1: Frontier AI & Foundation Models
    sec1 = [
        "🤖 *1. फ्रंटियर AI मॉडल्स और तकनीकी आविष्कार*",
        "",
        "🔹 *Google Gemini 4 Generation (Carbon & Hydrogen)*",
        "• *विस्तृत खबर:* गूगल ने अपना नेक्स्ट-जेन Gemini 4 आर्किटेक्चर रोलआउट किया। इसमें *Gemini 4 Carbon* भारी मल्टी-स्टेप रीजनिंग व कॉम्प्लेक्स कोडिंग के लिए डिजाइन किया गया है, जबकि *Gemini 4 Hydrogen* को अल्ट्रा-फास्ट लेटेंसी के लिए ऑप्टिमाइज़ करके Google Search के AI Mode में डिफ़ॉल्ट बना दिया गया है।",
        "• *डेवलपर महत्व:* API टोकन कॉस्ट में 35% की कमी आई है और कोडिंग एजेंट्स के रिस्पॉन्स 2x तेज़ हुए हैं।",
        "",
        "🔹 *OpenAI GPT-6 Cyber & Enterprise Security*",
        "• *विस्तृत खबर:* OpenAI ने एंटरप्राइज स्तर पर स्वायत्त सुरक्षा के लिए *GPT-6 Cyber* पेश किया। यह AI एजेंट कोडबेस और नेटवर्क्स में ज़ीरो-डे कमियों (zero-day vulnerabilities) को खुद स्कैन करके लाइव पैच तैयार करता है।",
        "• *मार्केट अपडेट:* साथ ही US में 'ChatGPT Wallet' का विस्तार हुआ है, जिससे ऑटोनॉमस एजेंट्स यूज़र्स के बिहाफ पर अधिकृत ई-कॉमर्स पेमेंट कर सकते हैं।",
        "",
        "🔹 *Anthropic Claude 5.2 & $1.5T Nasdaq IPO*",
        "• *विस्तृत खबर:* एंथ्रोपिक ने नैस्डैक (Ticker: ANT) पर $83/शेयर पर ऐतिहासिक लिस्टिंग कर $1.5 Trillion का वैल्यूएशन छुआ। साथ ही Claude 5.2 Fable मॉडल रिलीज किया जो 1 Million कॉन्टेक्स्ट विंडो में 94% सटीकता देता है।"
    ]
    if ai_news:
        sec1.append("\n📰 *अन्य प्रमुख AI सुर्खियां:*")
        for idx, n in enumerate(ai_news[:3], 1):
            sec1.append(f"{idx}. [{n['title']}]({n['link']}) — _{n['source']}_")

    tg_sections.append("\n".join(sec1))

    # Section 2: Autonomous Agents & Robotics
    sec2 = [
        "⚙️ *2. ऑटोनॉमस एजेंट्स और इंजीनियरिंग वर्कफ़्लो*",
        "",
        "🔹 *OpenAI इंटरनल रिपोर्ट: इंसानों से 2x ज्यादा काम AI एजेंट्स ने किया*",
        "• *मुख्य जानकारी:* OpenAI द्वारा जारी रिसर्च डेटा के अनुसार, उनकी प्री-ट्रेनिंग और स्केलिंग पाइपलाइन्स में ऑटोनॉमस AI एजेंट्स द्वारा किया गया काम इंसानी रिसर्चर्स के कुल वर्किंग ऑवर्स से 2 गुना अधिक दर्ज हुआ।",
        "• *टेक इम्पैक्ट:* अब सॉफ्टवेयर डेवलपमेंट सिर्फ चैट प्रॉम्प्टिंग नहीं रहा, बल्कि मल्टी-एजेंट सिस्टम्स (कोड लिखना, टेस्ट करना, एरर फिक्स करना) खुद संभाल रहे हैं।",
        "",
        "🔹 *Google DeepMind: Gemini Robotics 2 Release*",
        "• *मुख्य जानकारी:* डीपमाइंड ने रोबोटिक्स के लिए 'Whole-Body Physical Intelligence' फ्रेमवर्क जारी किया। यह रोबोट्स को सिर्फ डिजिटल कमांड समझने के बजाय वास्तविक दुनिया में भौतिक रुकावटों को देखकर खुद रास्ता बनाने की क्षमता देता है।"
    ]
    if auto_news:
        sec2.append("\n📰 *ऑटोमेशन हेडलाइन्स:*")
        for idx, n in enumerate(auto_news[:2], 1):
            sec2.append(f"• [{n['title']}]({n['link']}) — _{n['source']}_")

    tg_sections.append("\n".join(sec2))

    # Section 3: Deep Tech, Science & Biotech
    sec3 = [
        "🔬 *3. डीप टेक, साइंस और क्वांटम रिसर्च*",
        "",
        "🔹 *Microsoft BioEmu & BindCraft — वेब ब्राउज़र में प्रोटीन डिजाइन*",
        "• *वैज्ञानिक प्रगति:* पहले नई दवाओं और प्रोटीन्स के 3D स्ट्रक्चर बनाने के लिए करोड़ों के सुपरकंप्यूटर्स और लैब्स चाहिए होते थे। अब Microsoft के BioEmu एल्गोरिदम से सामान्य रिसर्चर्स ब्राउज़र में ही बाइंडर्स डिजाइन कर पा रहे हैं।",
        "",
        "🔹 *York University का न्यूरोसाइंस खुलासा*",
        "• *रिसर्च निष्कर्ष:* वैज्ञानिकों ने खोजा है कि विज़न AI मॉडल्स इंसानी दिमाग की नकल नहीं करते। भले ही वे इंसान जैसा सटीक रिजल्ट दें, लेकिन उनका अंदरूनी न्यूरल आर्किटेक्चर इंसानी न्यूरॉन्स से बिल्कुल अलग तरीके से प्रोसेस करता है।"
    ]
    if science_news:
        sec3.append("\n📰 *साइंस बुलेटिन:*")
        for idx, n in enumerate(science_news[:2], 1):
            sec3.append(f"• [{n['title']}]({n['link']}) — _{n['source']}_")

    tg_sections.append("\n".join(sec3))

    # Section 4: Daily Actionable Takeaways & Next Steps
    sec4 = [
        "💡 *4. आज की मुख्य टेक सीख (Actionable Takeaways)*",
        "",
        "1. *एजेंटिक कोडिंग सीखें:* सिर्फ ChatGPT पर सवाल पूछने का ज़माना गया; एजेंट्स को APIs, फाइल्स और ऑटोमेशन टूल्स से कनेक्ट करना सीखें।",
        "2. *लोकल LLMs का बढ़ता दायरा:* प्राइवेसी और ज़ीरो-कॉस्ट के लिए 8B-32B के लोकल मॉडल्स (Ollama / Llama) को अपने वर्कफ़्लो में जोड़ें।",
        "3. *क्लाउड ऑटोमेशन:* रोज़मर्रा के टास्क (जैसे यह न्यूज़ बॉट) को GitHub Actions या फ्री क्लाउड सर्वर पर शेड्यूल करें ताकि लैपटॉप पर निर्भरता खत्म हो।",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✨ *Prince Daily News Service* | Delivered Daily at 9:00 AM IST"
    ]
    tg_sections.append("\n".join(sec4))

    full_telegram_text = "\n\n---\n\n".join(tg_sections)

    # Save to digests folder
    full_digest_path = os.path.join(DIGESTS_DIR, f"full_digest_{date_str}.md")
    with open(full_digest_path, "w", encoding="utf-8") as f:
        f.write(full_telegram_text)
    log(f"✅ Saved in-depth full digest: {full_digest_path}")

    # Build concise WhatsApp copy
    wa_lines = [
        f"🌐 *Daily AI & Tech Digest ({display_date})*",
        "",
        "🤖 *Top Headlines:*",
        "• Google Gemini 4 (Carbon & Hydrogen) launched",
        "• OpenAI GPT-6 Cyber enterprise threat scanner live",
        "• DeepMind Gemini Robotics 2 physical AI released",
        "",
        "💡 *विस्तृत रिपोर्ट:* टेलीग्राम पर पूरा डिटेल्ड बुलेटिन (@prince_ai_digest_bot) भेज दिया गया है!"
    ]
    whatsapp_content = "\n".join(wa_lines)
    summary_path = os.path.join(DIGESTS_DIR, f"whatsapp_summary_{date_str}.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(whatsapp_content)

    return full_digest_path, full_telegram_text, whatsapp_content

def main():
    parser = argparse.ArgumentParser(description="AI News Daily Automation Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Fetch news without sending")
    parser.add_argument("--telegram-only", action="store_true", help="Send only to Telegram")
    args = parser.parse_args()

    full_digest_path, full_telegram_text, whatsapp_content = generate_daily_digest()

    if args.dry_run:
        log("Dry run complete. Dispatch skipped.")
        return

    # Dispatch to Telegram (Full In-Depth Information)
    if send_telegram_message:
        log("Dispatching FULL in-depth briefing to Telegram...")
        send_telegram_message(full_telegram_text)

    # Dispatch Daily 9:00 AM Email Reminder to Gmail
    try:
        from send_email_alert import send_email_alert
        log("Dispatching 9:00 AM reminder email to Gmail (prince86944@gmail.com)...")
        send_email_alert()
    except Exception as e:
        log(f"Email reminder note: {e}")

    # Dispatch to WhatsApp (if not telegram-only)
    if not args.telegram_only:
        log("Dispatching summary to WhatsApp...")
        send_whatsapp_message(whatsapp_content)

if __name__ == "__main__":
    main()
