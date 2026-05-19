from fpdf import FPDF
import os
from datetime import datetime


# ─── Palette ──────────────────────────────────────────────────────────────────
ACCENT = (216, 192, 247)  # #d8c0f7
BG_DARK     = (10,  10,  10)   # near-black
BG_LIGHT    = (247, 247, 245)  # off-white
GREY_DARK   = (40,  40,  40)   # body text
GREY_MID    = (120, 120, 120)  # muted text
GREY_LIGHT  = (230, 230, 228)  # subtle borders / dividers
WHITE       = (255, 255, 255)

# ─── Text Sanitiser ───────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2014": "-", "\u2013": "-",
        "\u2022": "-", "\u2026": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "ignore").decode("latin-1")


# ─── PDF Class ────────────────────────────────────────────────────────────────
class PDF(FPDF):

    def __init__(self, company: str, website: str):
        super().__init__()
        self.company = company
        self.website = website
        self.set_margins(20, 28, 20)
        self.set_auto_page_break(auto=True, margin=20)

    # ── Cover page ────────────────────────────────────────────────────────────
    def cover_page(self):
        self.add_page()

        # Full dark background
        self.set_fill_color(*BG_DARK)
        self.rect(0, 0, 210, 297, "F")

        # Lime accent strip at top
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, 210, 5, "F")

        # Label
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*ACCENT)

        self.cell(
            0,
            8,
            "AI GROWTH AUDIT",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        self.ln(6)

        # Company name
        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*WHITE)
        self.cell(0, 14, self.company, align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(4)

        # Website
        self.set_font("Helvetica", "", 12)
        self.set_text_color(*GREY_MID)
        self.cell(0, 8, self.website, align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(16)

        # Thin divider
        self.set_draw_color(*GREY_MID)
        cx = 210 / 2
        self.line(cx - 30, self.get_y(), cx + 30, self.get_y())

        self.ln(16)

        # Date
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*GREY_MID)
        date_str = datetime.now().strftime("%B %d, %Y")
        self.cell(0, 8, f"Generated {date_str}", align="C", new_x="LMARGIN", new_y="NEXT")

        # Bottom label
        self.set_y(-20)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GREY_MID)
        self.cell(0, 8, "CONFIDENTIAL", align="C")

    # ── Running header ────────────────────────────────────────────────────────
    def header(self):
        if self.page_no() == 1:
            return

        # Lime top bar
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, 210, 3, "F")

        # Header text
        self.set_y(7)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GREY_MID)
        self.cell(0, 6, f"AI GROWTH AUDIT  \u00b7  {self.company.upper()}", new_x="LMARGIN", new_y="NEXT")

        # Hairline separator
        self.set_draw_color(*GREY_LIGHT)
        self.line(self.l_margin, self.get_y(), 210 - self.r_margin, self.get_y())
        self.ln(6)

    # ── Running footer ────────────────────────────────────────────────────────
    def footer(self):
        if self.page_no() == 1:
            return

        self.set_y(-14)
        self.set_draw_color(*GREY_LIGHT)
        self.line(self.l_margin, self.get_y(), 210 - self.r_margin, self.get_y())
        self.ln(2)

        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GREY_MID)
        self.cell(0, 6, f"Page {self.page_no() - 1}", align="C")

    # ── Section heading ───────────────────────────────────────────────────────
    def chapter_title(self, title: str):
        # Lime left rule
        x = self.l_margin
        y = self.get_y()
        self.set_fill_color(*ACCENT)
        self.rect(x, y, 3, 10, "F")

        # Title text
        self.set_x(x + 7)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*BG_DARK)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    # ── Body paragraph ────────────────────────────────────────────────────────
    def chapter_body(self, body: str):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*GREY_DARK)
        self.multi_cell(0, 7, body)
        self.ln(3)

    # ── Subtle divider between sections ──────────────────────────────────────
    def section_divider(self):
        self.ln(2)
        self.set_draw_color(*GREY_LIGHT)
        self.line(self.l_margin, self.get_y(), 210 - self.r_margin, self.get_y())
        self.ln(6)


# ─── Heading Detection ────────────────────────────────────────────────────────
def is_heading(line: str) -> bool:
    stripped = line.lstrip("#").strip()
    return (
        line.startswith("#")
        or (stripped.isupper() and len(stripped) > 2)
        or (len(stripped) < 65 and stripped.endswith(":") and stripped[0].isupper())
    )


# ─── Public API ───────────────────────────────────────────────────────────────
def generate_pdf(report: str, company: str, website: str = "") -> str:
    report = clean_text(report)

    pdf = PDF(company=company, website=website)

    # Cover
    pdf.cover_page()

    # Content pages
    pdf.add_page()

    prev_was_heading = False

    for line in report.split("\n"):
        line = line.strip()
        if not line:
            continue

        if is_heading(line):
            if not prev_was_heading:
                pdf.section_divider()
            pdf.chapter_title(line.lstrip("#").strip().rstrip(":"))
            prev_was_heading = True
        else:
            pdf.chapter_body(line)
            prev_was_heading = False

    os.makedirs("reports", exist_ok=True)
    filename = f"{company.replace(' ', '_')}_audit.pdf"
    path = os.path.join("reports", filename)
    pdf.output(path)

    return path