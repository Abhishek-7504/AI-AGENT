import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

class EmailAgent:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, to_email, subject, summary, task):
        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = to_email
        msg["Subject"] = subject

        body = f"""
        Hello,

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
            print(f"✅ Email sent to {to_email}")
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
