import os
import sys
import time
import re
import subprocess
from send_telegram import save_config, send_telegram_message, auto_detect_chat_id, load_config

TOKEN_REGEX = re.compile(r"^[0-9]{8,11}:[a-zA-Z0-9_-]{35}$")

def open_botfather():
    print("🚀 Opening BotFather in Telegram Desktop...")
    try:
        os.system("start tg://resolve?domain=BotFather")
    except Exception as e:
        print("Note:", e)

def get_token_from_clipboard():
    try:
        import win32clipboard
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data.strip()
    except Exception:
        pass
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return ""

def main():
    print("=" * 60)
    print("🤖 TELEGRAM BOT AUTO-SETUP WIZARD")
    print("=" * 60)
    
    open_botfather()
    
    print("\n👉 BotFather aapke screen par khul chuka hai.")
    print("1. Wahan likhein: /newbot")
    print("2. Koi bhi Name dein (e.g. Prince Daily News)")
    print("3. Ek unique username dein jiske end me 'bot' ho (e.g. prince_daily_ai_bot)")
    print("4. BotFather jo Token dega, use Copy kar lein (Ctrl+C).\n")
    print("⏳ Clipboard monitor ho raha hai... Jaise hi aap Copy karenge, auto-setup shuru ho jayega!")
    
    token = None
    start_time = time.time()
    
    # Check clipboard for up to 60 seconds
    while time.time() - start_time < 90:
        clip = get_token_from_clipboard()
        if clip and ":" in clip and len(clip) > 30 and (TOKEN_REGEX.match(clip) or (":" in clip and clip.split(":")[0].isdigit())):
            token = clip
            print(f"\n🎉 Token auto-detected from clipboard: {token[:6]}...{token[-4:]}")
            break
        time.sleep(1.5)
        
    if not token:
        # Prompt manual if not found
        try:
            token = input("\nAap yahan direct Token paste karein: ").strip()
        except Exception:
            pass

    if not token:
        print("❌ Token nahi mila. Kripya token copy karke dubara run karein.")
        return

    save_config(token)
    print("✅ Token successfully save ho gaya hai!")
    
    print("\n👉 Aakhiri Step: Apne naye bane bot ko start karein:")
    print("   Telegram me apne bot ka link open karein aur 'START' button dabayein.")
    print("⏳ Chat ID auto-detect hone ka intezar kar rahe hain...")
    
    chat_id = None
    for attempt in range(1, 15):
        chat_id = auto_detect_chat_id(token)
        if chat_id:
            break
        time.sleep(3)
        
    if chat_id:
        print(f"\n🎉 Chat ID mil gaya: {chat_id}")
        print("Sending test message...")
        send_telegram_message("🚀 *Daily AI News Automation Active!*\n\nनमस्ते प्रिंस! आपका टेलीग्राम ऑटोमेशन पूरी तरह चालू हो गया है। अब हर सुबह 9:00 बजे ताज़ा AI व टेक डाइजेस्ट सीधे यहाँ आएगा। ✅")
    else:
        print("\nℹ️ Token save ho chuka hai. Jab aap bot me 'Start' dabayenge, pehla message aate hi chat ID set ho jayegi.")

if __name__ == "__main__":
    main()
