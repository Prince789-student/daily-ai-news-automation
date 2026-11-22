import time
import json
import os
import urllib.request
from send_telegram import auto_detect_chat_id, send_telegram_message, save_config

TOKEN = "9257539042:AAHZk7ijbvyWbsCydhnoZg5wtg583mce1wk"

print("Listening for START on @prince_ai_digest_bot (up to 10 minutes)...")

chat_id = None
for i in range(300): # 10 minutes
    chat_id = auto_detect_chat_id(TOKEN)
    if chat_id:
        break
    time.sleep(2)

if chat_id:
    print(f"🎉 Chat ID detected: {chat_id}!")
    save_config(TOKEN, chat_id)
    
    # Send test greeting
    test_msg = (
        "🚀 *Prince Daily News Bot Active!*\n\n"
        "नमस्ते प्रिंस! आपका पर्सनल टेलीग्राम AI न्यूज़ बॉट पूरी तरह कनेक्ट हो चुका है। ✅\n\n"
        "📅 *शेड्यूल:* रोज़ाना सुबह ठीक *9:00 AM IST* पर ताज़ा AI, साइंस और टेक न्यूज़ सीधे आपको यहाँ मिलेगी (चाहे आपका लैपटॉप बंद रहे या चालू)!"
    )
    send_telegram_message(test_msg, token=TOKEN, chat_id=chat_id)
    
    # Read today's summary and send it too!
    today_summary_path = os.path.join(os.path.dirname(__file__), "digests", "whatsapp_summary_2026_11_22.txt")
    if os.path.exists(today_summary_path):
        with open(today_summary_path, "r", encoding="utf-8") as f:
            digest_text = f.read()
        time.sleep(1)
        send_telegram_message(f"📰 *Today's AI & Tech Digest:*\n\n{digest_text}", token=TOKEN, chat_id=chat_id)
        print("✅ Today's digest delivered to Telegram!")
else:
    print("⏳ Timeout waiting for START.")
