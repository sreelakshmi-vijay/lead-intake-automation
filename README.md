# AI Lead Intake Automation

> [!NOTE]
Technical Assessment Submission
This project was built as part of the technical assessment for the AI Software Developer Intern position at SimplifiIQ. It represents my solution to the provided assessment brief and is submitted via the required Google Form.

> Drop in a lead's name, email, and website — get a personalized AI audit report delivered straight to your inbox.

---

## What It Does

This tool automates the entire lead nurturing workflow in four steps:

1. **Scrapes** the prospect's website for key content (title, description, headings)
2. **Generates** a structured AI audit report using a local Ollama model (phi3)
3. **Renders** the report as a polished PDF via WeasyPrint
4. **Emails** the PDF directly to the lead — automatically

All of this happens in a background thread the moment a form is submitted, so the response is instant and the heavy lifting runs silently behind the scenes.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Web framework | Flask |
| Web scraping | Requests + BeautifulSoup4 |
| AI generation | Ollama (phi3) |
| PDF rendering | WeasyPrint |
| Email delivery | smtplib (Gmail SMTP) |
| Environment config | python-dotenv |

---

## Project Structure

```
├── app.py                  # Flask app + background processing pipeline
├── templates/
│   └── index.html          # Lead intake form
├── static/
│   ├── style.css
│   └── script.js
├── services/
│   ├── scrapper.py         # Website scraping
│   ├── ai_report.py        # Ollama report generation
│   ├── pdf_generator.py    # PDF creation
│   └── email_sender.py     # Gmail delivery
├── reports/                # Generated PDF output
└── requirements.txt
```

---

## Setup

**1. Clone and install dependencies**

```bash
pip install -r services/requirements.txt
```

**2. Install and run Ollama with the phi3 model**

```bash
ollama pull phi3
ollama serve
```

**3. Configure your email credentials**

Create a `.env` file in the project root:

```
EMAIL=your@gmail.com
PASSWORD=your_app_password
```

> Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your regular account password.

**4. Run the app**

```bash
python app.py
```

Visit `http://localhost:5000`, fill in a lead's details, and watch the pipeline do its thing.

---

## How the Pipeline Works

```
Form submission
    └─► scrape_company(website)
            └─► generate_ai_report(company_data)
                    └─► generate_pdf(report, company)
                            └─► send_email(email, pdf_path)
```

Each step logs its progress with a timestamp so you can follow along in the terminal.

---

## The AI Report Format

Every generated report follows a consistent structure:

- **Business Summary**
- **Website Strengths**
- **Website Weaknesses**
- **SEO Improvements**
- **Growth Opportunities**
- **Automation Suggestions**
- **Personalized Outreach**

Reports are grounded in the actual content scraped from the prospect's site, making each one genuinely specific to that company.

---

## Visuals
1. Terminal - Run App
<img width="1073" height="154" alt="Screenshot 2026-05-19 151616" src="https://github.com/user-attachments/assets/5409d21c-cda8-4d14-8f8b-e5ba60607766" />
2. Website - Landing Page
<img width="1919" height="940" alt="Screenshot 2026-05-19 151559" src="https://github.com/user-attachments/assets/62505045-e68e-4fc0-8ce1-3a90e22db9e2" />
3. Website - Form Details
<img width="1183" height="584" alt="Simplifi-IQ Assessment Output" src="https://github.com/user-attachments/assets/c114e203-b0a3-4f3a-b038-15161cb2695b" />
4. Website - Form Submitted
<img width="1917" height="944" alt="Screenshot 2026-05-19 155118" src="https://github.com/user-attachments/assets/50bca3e1-5aac-482e-b700-46b636534c1e" />
5. Recieved Mail
<img width="1587" height="488" alt="Screenshot 2026-05-19 153049" src="https://github.com/user-attachments/assets/cea3c2a8-7802-4934-ad49-bc19d66152b8" />
6. Generated Report Pages
<img width="1920" height="546" alt="Simplifi-IQ Assessment Output" src="https://github.com/user-attachments/assets/522d4d94-fa66-4fba-9c23-9897ce15f237" />

---

## Notes

- The processing pipeline runs in a background thread — the API responds immediately while the report is being generated
- PDF files are saved to the `reports/` directory before being emailed
