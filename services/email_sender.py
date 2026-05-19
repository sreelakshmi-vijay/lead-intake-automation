import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email, pdf_path):
    
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    msg = EmailMessage()

    msg["Subject"] = "Your AI Business Audit"
    msg["From"] = EMAIL
    msg["To"] = to_email

    msg.set_content(
        "Attached is your personalized audit report."
    )

    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="audit.pdf"
        )

    try:

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(EMAIL, PASSWORD)

            smtp.send_message(msg)

            print("✅ Email sent successfully")

    except Exception as e:

        print("❌ Email failed")
        print(e)