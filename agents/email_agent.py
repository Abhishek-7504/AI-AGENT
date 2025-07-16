import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from dotenv import load_dotenv
from pathlib import Path

class EmailAgent:
    def __init__(self, user_email_map=None):
        load_dotenv()
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        # ✅ Use dynamic email map if provided, otherwise load from file
        if user_email_map:
            self.user_email_map = user_email_map
        else:
            self.user_email_map = self.load_email_map()

    def load_email_map(self):
        email_file = Path("emails.json")
        if not email_file.exists():
            print("⚠️ 'emails.json' not found — proceeding with empty mapping.")
            return {}
        with open(email_file, "r") as f:
            return json.load(f)

    def send_personalized_email(self, name, subject, summary, task):
        to_email = self.user_email_map.get(name)
        if not to_email:
            print(f"[ERROR] No email found for '{name}'. Email not sent.")
            return

        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = to_email
        msg["Subject"] = subject

        body = f"""
        Hello {name},

        Here's a quick summary of the meeting:

        {summary}

        Your assigned action item:
        → {task}

        Regards,
        SmartMeet AI
        """

        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent to {name} at {to_email}")
        except Exception as e:
            print(f"[ERROR] Failed to send email to {name} ({to_email}): {e}")
