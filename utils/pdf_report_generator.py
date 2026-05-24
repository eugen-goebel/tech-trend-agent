"""PDF report generator for technology trend reports using fpdf2."""

import os
from datetime import datetime

from fpdf import FPDF

from agents.analyst import TechAnalysisResult
from utils.chart_generator import (
    create_key_players_chart,
    create_use_case_impact_chart,
)


_UNICODE_REPLACEMENTS = {
    "–": "-",
    "—": "--",
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    "…": "...",
    "•": "-",
    "€": "EUR",
    "ü": "ue",
    "ä": "ae",
    "ö": "oe",
    "Ü": "Ue",
    "Ä": "Ae",
    "Ö": "Oe",
    "ß": "ss",
}

IMPACT_COLORS = {
    "High": (198, 40, 40),
    "Medium": (230, 142, 0),
    "Low": (13, 115, 119),
}


def _sanitize(text: str) -> str:
    """Coerce text to latin-1 so fpdf2 with Helvetica can render it."""
    if text is None:
        return ""
    for char, replacement in _UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    return text.encode("latin-1", errors="replace").decode("latin-1")


class _TrendReportPDF(FPDF):

    def __init__(self, title: str):
        super().__init__()
        self._doc_title = title

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, _sanitize(f"{self._doc_title}  |  Page {self.page_no()}"), align="C")


# ---------------------------------------------------------------------------
# Section helpers
# ---------------------------------------------------------------------------

def _heading(pdf: FPDF, text: str, size: int = 14):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", size)
    pdf.set_text_color(13, 115, 119)
    pdf.cell(0, 10, _sanitize(text), new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)


def _paragraph(pdf: FPDF, text: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, _sanitize(text))
    pdf.ln(2)


def _bullets(pdf: FPDF, items: list[str]):
    pdf.set_font("Helvetica", "", 10)
    for item in items:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, 5, _sanitize(f"   - {item}"))
    pdf.ln(2)


def _add_cover(pdf: FPDF, technology: str, analysis: TechAnalysisResult):
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(13, 115, 119)
    pdf.multi_cell(0, 12, _sanitize(f"{technology}"), align="C")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Technology Trend Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 6, _sanitize(datetime.now().strftime("%B %Y")), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(0, 0, 0)

    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    _paragraph(pdf, analysis.executive_summary)


def _add_overview(pdf: FPDF, analysis: TechAnalysisResult):
    pdf.add_page()
    _heading(pdf, "Technology Overview")
    _paragraph(pdf, analysis.technology_overview)
    _heading(pdf, "Maturity Assessment", size=12)
    _paragraph(pdf, analysis.maturity_assessment)
    _heading(pdf, "Market Landscape", size=12)
    _paragraph(pdf, analysis.market_landscape)


def _add_key_players(pdf: FPDF, analysis: TechAnalysisResult, chart_path: str | None):
    pdf.add_page()
    _heading(pdf, "Key Players")
    if chart_path and os.path.exists(chart_path):
        pdf.image(chart_path, w=170)
        pdf.ln(4)
    for player in analysis.key_players:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, _sanitize(player.name), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, _sanitize(f"{player.focus_area}  |  {player.market_position}"), new_x="LMARGIN", new_y="NEXT")
        _paragraph(pdf, player.description)


def _add_use_cases(pdf: FPDF, analysis: TechAnalysisResult, chart_path: str | None):
    pdf.add_page()
    _heading(pdf, "Use Cases")
    if chart_path and os.path.exists(chart_path):
        pdf.image(chart_path, w=170)
        pdf.ln(4)
    for uc in analysis.use_cases:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, _sanitize(uc.title), new_x="LMARGIN", new_y="NEXT")
        color = IMPACT_COLORS.get(uc.impact_level, (120, 120, 120))
        pdf.set_text_color(*color)
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, _sanitize(f"Impact: {uc.impact_level}  |  Industry: {uc.industry}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        _paragraph(pdf, uc.description)


def _add_strategic_outlook(pdf: FPDF, analysis: TechAnalysisResult):
    pdf.add_page()
    _heading(pdf, "Strategic Outlook")
    _paragraph(pdf, analysis.future_outlook)

    _heading(pdf, "Strengths", size=12)
    _bullets(pdf, analysis.strengths)

    _heading(pdf, "Limitations", size=12)
    _bullets(pdf, analysis.limitations)

    _heading(pdf, "Adoption Drivers", size=12)
    _bullets(pdf, analysis.adoption_drivers)

    _heading(pdf, "Adoption Barriers", size=12)
    _bullets(pdf, analysis.adoption_barriers)

    _heading(pdf, "Key Trends", size=12)
    _bullets(pdf, analysis.key_trends)

    _heading(pdf, "Risk Factors", size=12)
    _bullets(pdf, analysis.risk_factors)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _materialize_chart(buf, output_dir: str, name: str) -> str | None:
    """Persist a BytesIO chart to disk and return the file path."""
    if buf is None:
        return None
    chart_dir = os.path.join(output_dir, "charts")
    os.makedirs(chart_dir, exist_ok=True)
    path = os.path.join(chart_dir, name)
    buf.seek(0)
    with open(path, "wb") as f:
        f.write(buf.read())
    return path


def generate_pdf_report(
    technology: str,
    analysis: TechAnalysisResult,
    output_dir: str,
) -> str:
    """Generate a single-technology PDF trend report and return its path."""
    os.makedirs(output_dir, exist_ok=True)

    players_chart = _materialize_chart(
        create_key_players_chart(analysis), output_dir, "key_players.png"
    )
    use_case_chart = _materialize_chart(
        create_use_case_impact_chart(analysis), output_dir, "use_case_impact.png"
    )

    pdf = _TrendReportPDF(title=f"{technology} Trend Report")
    pdf.set_auto_page_break(auto=True, margin=20)

    _add_cover(pdf, technology, analysis)
    _add_overview(pdf, analysis)
    _add_key_players(pdf, analysis, players_chart)
    _add_use_cases(pdf, analysis, use_case_chart)
    _add_strategic_outlook(pdf, analysis)

    safe_name = technology.lower().replace(" ", "_").replace("/", "_")
    filename = f"trend_report_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)
    return filepath


def generate_comparison_pdf_report(
    technologies: list[str],
    analyses: list[TechAnalysisResult],
    output_dir: str,
) -> str:
    """Generate a side-by-side comparison PDF and return its path."""
    if len(technologies) != len(analyses):
        raise ValueError("technologies and analyses must have the same length")
    os.makedirs(output_dir, exist_ok=True)

    pdf = _TrendReportPDF(title="Tech Comparison Report")
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- Cover ---
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(13, 115, 119)
    pdf.multi_cell(0, 12, _sanitize("Technology Comparison Report"), align="C")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 7, _sanitize(" vs ".join(technologies)), align="C")
    pdf.set_text_color(0, 0, 0)

    # --- Per-technology sections ---
    for tech, analysis in zip(technologies, analyses):
        pdf.add_page()
        _heading(pdf, tech, size=16)
        _heading(pdf, "Executive Summary", size=12)
        _paragraph(pdf, analysis.executive_summary)
        _heading(pdf, "Maturity", size=12)
        _paragraph(pdf, analysis.maturity_assessment)
        _heading(pdf, "Key Players", size=12)
        _bullets(pdf, [f"{p.name} - {p.focus_area}" for p in analysis.key_players])
        _heading(pdf, "Top Use Cases", size=12)
        _bullets(pdf, [f"{u.title} ({u.impact_level}) - {u.industry}" for u in analysis.use_cases])
        _heading(pdf, "Strengths", size=12)
        _bullets(pdf, analysis.strengths)
        _heading(pdf, "Limitations", size=12)
        _bullets(pdf, analysis.limitations)

    safe_techs = "_vs_".join(t.lower().replace(" ", "_") for t in technologies)
    filename = f"comparison_{safe_techs}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)
    return filepath
