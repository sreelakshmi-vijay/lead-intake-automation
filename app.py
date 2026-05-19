from flask import Flask, render_template, request, jsonify
from threading import Thread
from datetime import datetime

from services.scrapper import scrape_company
from services.ai_report import generate_ai_report
from services.pdf_generator import generate_pdf
from services.email_sender import send_email

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


def process_lead(data):

    try:

        name = data.get("name")
        email = data.get("email")
        company = data.get("company")
        website = data.get("website")

        # START LOG
        print(f"[{datetime.now()}] Started processing: {company}")

        # 1. Scrape company
        company_data = scrape_company(website)

        print(f"[{datetime.now()}] Scraping completed")

        # 2. Generate AI report
        report = generate_ai_report(company_data)

        print(f"[{datetime.now()}] AI report generated")

        # 3. Generate PDF
        pdf_path = generate_pdf(report, company)

        print(f"[{datetime.now()}] PDF generated")

        # 4. Send email
        send_email(email, pdf_path)

        print(f"[{datetime.now()}] Email sent successfully")

        print(f"[{datetime.now()}] Finished processing: {company}")

    except Exception as e:

        print(f"[{datetime.now()}] PROCESS ERROR:", e)


@app.route("/submit", methods=["POST"])
def submit():

    data = request.json

    thread = Thread(
        target=process_lead,
        args=(data,)
    )

    thread.start()

    return jsonify({
        "success": True,
        "message": "Audit request submitted successfully."
    })


if __name__ == "__main__":
    app.run(debug=True)