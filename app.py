from flask import Flask, render_template, request, jsonify
from services.scrapper import scrape_company
from services.ai_report import generate_ai_report
from services.pdf_generator import generate_pdf
from services.email_sender import send_email

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/submit", methods=["POST"])
def submit():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    company = data.get("company")
    website = data.get("website")

    # 1. Scrape website
    company_data = scrape_company(website)

    # 2. Generate AI report
    report = generate_ai_report(company_data)

    # 3. Generate PDF
    pdf_path = generate_pdf(report, company)

    # 4. Send email
    send_email(email, pdf_path)

    return jsonify({
        "message": "Audit generated successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)