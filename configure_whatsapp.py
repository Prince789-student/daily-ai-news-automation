import sys
import os
import argparse
from send_whatsapp import load_config, save_config, send_whatsapp_message, CONFIG_FILE

def show_status():
    config = load_config()
    phone = config.get("phone", "")
    apikey = config.get("apikey", "")
    print("=" * 60)
    print("📱 WhatsApp Configuration Status")
    print("=" * 60)
    print(f"Config File: {CONFIG_FILE}")
    if phone and apikey:
        masked_key = apikey[:2] + "****" + apikey[-2:] if len(apikey) > 4 else "****"
        print(f"Phone Number: {phone}")
        print(f"API Key:      {masked_key}")
        print("Status:       ✅ Configured")
    else:
        print("Phone Number: [Not Set]")
        print("API Key:      [Not Set]")
        print("Status:       ⚠️ Incomplete (Setup Required)")
        print("\n👉 Setup Steps:")
        print("1. WhatsApp par +34 623 78 64 49 par message karein:")
        print("   'I allow callmebot to send me messages'")
        print("   Direct link: https://wa.me/34623786449?text=I%20allow%20callmebot%20to%20send%20me%20messages")
        print("2. CallMeBot aapko reply me ek API Key dega.")
        print("3. Yeh command chalayein:")
        print("   python configure_whatsapp.py --phone \"+91XXXXXXXXXX\" --apikey \"APPIKEY\"")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Configure WhatsApp settings for AI News Automation")
    parser.add_argument("--phone", help="Phone number with country code, e.g. +91XXXXXXXXXX")
    parser.add_argument("--apikey", help="CallMeBot API key")
    parser.add_argument("--status", action="store_true", help="Display current configuration status")
    parser.add_argument("--test", action="store_true", help="Send a test message to verify setup")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.phone and args.apikey:
        save_config(args.phone, args.apikey)
        print(f"\n✅ WhatsApp configuration saved successfully!")
        print(f"📱 Phone: {args.phone}")
        print(f"🔑 API Key: {args.apikey}")
        print("\nSending test message to WhatsApp...")
        test_msg = "🤖 *AI News Automation Test*\n\nAapka WhatsApp configuration safaltapoorvak set ho gaya hai! Ab daily tech digests seedhe yahan aayenge. ✅"
        success = send_whatsapp_message(test_msg, phone=args.phone, apikey=args.apikey)
        if success:
            print("🎉 Test message WhatsApp par deliver ho gaya!")
        else:
            print("⚠️ Test message deliver nahi ho saka. Kripya check karein ki phone number aur API key sahi hain.")
        return

    if args.test:
        config = load_config()
        if not config.get("phone") or not config.get("apikey"):
            print("❌ Phone ya API Key set nahi hai. Pehle configure karein:")
            print("   python configure_whatsapp.py --phone \"+91...\" --apikey \"...\"")
            return
        print("Sending test message...")
        test_msg = "🤖 *AI News Automation Test*: System is active and ready! ✅"
        send_whatsapp_message(test_msg)
        return

    # If no flags provided, run interactive setup
    print("\n" + "=" * 60)
    print("🤖 WhatsApp Setup Wizard for AI News Automation")
    print("=" * 60)
    show_status()
    print()
    
    try:
        phone_input = input("Apna Phone Number daalein (+91... format) [Enter dabayein skip karne ke liye]: ").strip()
        if not phone_input:
            print("Setup cancelled.")
            return
            
        apikey_input = input("CallMeBot API Key daalein: ").strip()
        if not apikey_input:
            print("Setup cancelled.")
            return
            
        save_config(phone_input, apikey_input)
        print("\n✅ Configuration save ho gayi hai!")
        
        do_test = input("Kya aap test message bhejna chahte hain? (y/n) [y]: ").strip().lower()
        if do_test in ("", "y", "yes"):
            test_msg = "🤖 *AI News Automation Test*: Configuration successful! ✅"
            send_whatsapp_message(test_msg, phone=phone_input, apikey=apikey_input)
    except (KeyboardInterrupt, EOFError):
        print("\nSetup cancelled.")

if __name__ == "__main__":
    main()
