from fpdf import FPDF
import os


class PDF(FPDF):

    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 15, "AI Business Audit", ln=True)

        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, "Generated Automatically", ln=True)

        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.multi_cell(0, 10, title)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, body)
        self.ln()


def generate_pdf(report, company):

    pdf = PDF()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    sections = report.split("\n")

    for section in sections:

        if section.strip() == "":
            continue

        # Headings
        if ":" not in section and len(section) < 60:
            pdf.chapter_title(section)

        else:
            pdf.chapter_body(section)

    os.makedirs("reports", exist_ok=True)

    filename = f"{company.replace(' ', '_')}.pdf"

    path = os.path.join("reports", filename)

    pdf.output(path)

    return path