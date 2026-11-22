import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

RECIPIENT_EMAIL = "prince86944@gmail.com"

def send_email_alert(subject="🔔 Daily AI News Alert: Telegram open karke check kar lo!", custom_message=None):
    print(f"📧 Preparing 9:00 AM Email Notification for {RECIPIENT_EMAIL}...")
    
    body = custom_message or (
        "Namaste Prince bhai!\n\n"
        "⏰ Subah ke 9:00 AM baj chuke hain!\n\n"
        "Aaj ka Daily AI & Tech News Digest, Tech Leaders (Elon Musk, Mark Zuckerberg, Sam Altman, Jensen Huang) ke live updates, "
        "aur Instagram Creators (its_anmol.ai, baljeet.ai, inder.code, tech.vision24) ke naye AI Tools & Videos aapke Telegram Bot par deliver ho chuke hain.\n\n"
        "👉 Abhi Telegram open karke check kar lo:\n"
        "https://t.me/prince_ai_digest_bot\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🤖 Prince Daily News Automation Cloud System\n"
        "⚡ 100% Cloud-Powered by GitHub Actions"
    )

    # Method 1: Direct Gmail SMTP SSL (if App Password is provided)
    gmail_pass = os.environ.get("GMAIL_APP_PASSWORD")
    if gmail_pass:
        try:
            msg = MIMEMultipart()
            msg["From"] = f"Prince AI Bot <{RECIPIENT_EMAIL}>"
            msg["To"] = RECIPIENT_EMAIL
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
                server.login(RECIPIENT_EMAIL, gmail_pass)
                server.sendmail(RECIPIENT_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            print(f"✅ Email successfully delivered via Gmail SMTP to {RECIPIENT_EMAIL}!")
            return True
        except Exception as e:
            print(f"⚠️ Gmail SMTP attempt note: {e}")

    # Method 2: FormSubmit Cloud Email Relay (Zero credentials, free cloud email)
    url = f"https://formsubmit.co/ajax/{RECIPIENT_EMAIL}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://prince-ai-news.github.io/",
        "Origin": "https://prince-ai-news.github.io"
    }
    data = {
        "name": "Prince AI Daily News System",
        "_subject": subject,
        "message": body
    }
    try:
        res = requests.post(url, headers=headers, json=data, timeout=20)
        print(f"FormSubmit Response ({res.status_code}): {res.text}")
        if res.status_code == 200:
            print(f"✅ Email alert dispatched to {RECIPIENT_EMAIL}!")
            return True
    except Exception as e:
        print(f"❌ FormSubmit error: {e}")

    return False

if __name__ == "__main__":
    send_email_alert()
