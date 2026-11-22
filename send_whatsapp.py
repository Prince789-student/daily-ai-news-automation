import sys
import json
import os
import urllib.parse
import urllib.request
import time

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "whatsapp_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(phone, apikey):
    config = {
        "phone": str(phone).strip(),
        "apikey": str(apikey).strip(),
        "instructions": (
            "1. WhatsApp par +34 623 78 64 49 par message bhejein: 'I allow callmebot to send me messages'\n"
            "2. CallMeBot aapko ek apikey reply karega.\n"
            "3. Apna phone number (jaise +91XXXXXXXXXX) aur apikey yahan daalein."
        )
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    return config

def send_via_local_bot(text, phone=None):
    clean_phone = str(phone).replace("+", "").replace(" ", "").replace("-", "").strip() if phone else None
    payload = {
        "message": text,
        "phone": clean_phone
    }
    data = json.dumps(payload).encode("utf-8")

    # Retry up to 5 times (total ~35 seconds) to catch the active WhatsApp connection window
    for attempt in range(1, 6):
        try:
            req = urllib.request.Request(
                "http://localhost:3001/api/send-custom",
                data=data,
                headers={"Content-Type": "application/json", "User-Agent": "AINewsAutomation/1.0"}
            )
            with urllib.request.urlopen(req, timeout=20) as res:
                resp = json.loads(res.read().decode("utf-8"))
                if resp.get("success"):
                    print(f"✅ Personal WhatsApp ({clean_phone or 'Direct'}) par message safaltapoorvak bhej diya gaya hai!")
                    return True
                else:
                    reason = resp.get("reason", "Unknown error")
                    print(f"⏳ Attempt {attempt}/5: Bot connection check ({reason}). Retrying in 7 seconds...")
                    time.sleep(7)
        except Exception as e:
            print(f"⏳ Attempt {attempt}/5: Server waiting ({e}). Retrying in 7 seconds...")
            time.sleep(7)

    return False

def send_via_callmebot(text, target_phone, target_key):
    clean_phone = str(target_phone).replace("+", "").replace(" ", "").replace("-", "").strip()
    
    # Split text into chunks if it exceeds 1200 chars to avoid URL length limits
    max_chunk_size = 1200
    chunks = []
    if len(text) <= max_chunk_size:
        chunks = [text]
    else:
        lines = text.split("\n")
        current_chunk = []
        current_len = 0
        for line in lines:
            if current_len + len(line) + 1 > max_chunk_size:
                if current_chunk:
                    chunks.append("\n".join(current_chunk))
                    current_chunk = [line]
                    current_len = len(line)
                else:
                    chunks.append(line[:max_chunk_size])
                    current_chunk = [line[max_chunk_size:]]
                    current_len = len(current_chunk[0])
            else:
                current_chunk.append(line)
                current_len += len(line) + 1
        if current_chunk:
            chunks.append("\n".join(current_chunk))
            
    success_all = True
    for i, chunk in enumerate(chunks, 1):
        encoded_text = urllib.parse.quote(chunk)
        url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={target_key}"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            with urllib.request.urlopen(req, timeout=25) as res:
                resp_body = res.read().decode("utf-8")
                if len(chunks) > 1:
                    print(f"✅ Message Part {i}/{len(chunks)} Status: {resp_body}")
                    time.sleep(1.5)  # Pause between multi-part messages
                else:
                    print("✅ Message Delivery Status:", resp_body)
        except Exception as e:
            print(f"❌ Failed to deliver message part {i}/{len(chunks)}: {e}", file=sys.stderr)
            success_all = False
            
    return success_all

def send_whatsapp_message(text, phone=None, apikey=None):
    config = load_config()
    target_phone = phone or config.get("phone")
    target_key = apikey or config.get("apikey")
    
    # Priority 1: If CallMeBot API key & phone are set, send directly to personal WhatsApp
    if target_phone and target_key:
        print(f"📱 CallMeBot ke dwara Personal WhatsApp ({target_phone}) par bhej rahe hain...")
        return send_via_callmebot(text, target_phone, target_key)

    # Priority 2: Use local WhatsApp bot configured for personal chat (toMe or target phone)
    print("🔍 Local WhatsApp Bot se Personal chat par bhejne ki koshish kar rahe hain...")
    if send_via_local_bot(text, phone=target_phone):
        return True

    print("\n❌ [Personal WhatsApp Setup Required]")
    print("Aapko personal WhatsApp par daily news paane ke liye 2 aasan vikalp hain:")
    print("1. CallMeBot (Sabse recommended aur reliable personal setup):")
    print("   - WhatsApp par +34 623 78 64 49 par message karein: 'I allow callmebot to send me messages'")
    print("   - Jo apikey milega, use save karein:")
    print("     python configure_whatsapp.py --phone \"+91XXXXXXXXXX\" --apikey \"YOUR_APIKEY\"")
    print("2. Local Bot: Apna personal number whatsapp_config.json me daalein.")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--file" and len(sys.argv) > 2:
            file_path = sys.argv[2]
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    message = f.read()
            else:
                print(f"Error: File '{file_path}' not found.", file=sys.stderr)
                sys.exit(1)
        else:
            message = " ".join(sys.argv[1:])
        send_whatsapp_message(message)
    else:
        print("Usage: python send_whatsapp.py <message> OR python send_whatsapp.py --file <path_to_text_file>")
