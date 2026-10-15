"""
Professional Health Assessment PDF Report Generator using ReportLab
"""
import io
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from app.config import settings
from app.utils.image_utils import create_safe_thumbnail_bytes
import logging

logger = logging.getLogger(__name__)

# Primary Palette
COLOR_PRIMARY = colors.HexColor("#14532d")     # Deep Forest Green
COLOR_SECONDARY = colors.HexColor("#16a34a")   # Leaf Green
COLOR_ACCENT_BG = colors.HexColor("#f0fdf4")   # Soft Tint Green
COLOR_DARK_TEXT = colors.HexColor("#1e293b")   # Slate 800
COLOR_MUTED = colors.HexColor("#64748b")       # Slate 500
COLOR_BORDER = colors.HexColor("#cbd5e1")      # Slate 300
COLOR_AMBER = colors.HexColor("#d97706")       # Amber warning
COLOR_RED = colors.HexColor("#dc2626")         # Red error


class NumberedCanvas(canvas.Canvas):
    """Canvas that performs a two-pass calculation to draw 'Page X of Y' in the footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)

        # Bottom divider line
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(40, 42, letter[0] - 40, 42)

        # Footer text
        footer_text = "MangoCare AI — Preliminary Screening Report | Educational & Decision-Support Only"
        self.drawString(40, 28, footer_text)

        # Page numbering
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 28, page_str)

        self.restoreState()


class ReportService:
    """Generates official downloadable PDF assessment reports."""

    def __init__(self):
        self.report_dir = settings.REPORT_DIR
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf_report(
        self,
        analysis_data: Dict[str, Any],
        image_bytes: Optional[bytes] = None
    ) -> Path:
        """
        Creates a PDF document for the given analysis record.
        Returns the path to the generated PDF.
        """
        analysis_id = analysis_data["analysis_id"]
        pdf_filename = f"MangoCare_Report_{analysis_id}.pdf"
        output_path = self.report_dir / pdf_filename

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=55
        )

        styles = getSampleStyleSheet()

        # Custom Typography Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=COLOR_PRIMARY
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=COLOR_MUTED
        )
        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=COLOR_PRIMARY,
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "BodyDark",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=COLOR_DARK_TEXT
        )
        body_bold = ParagraphStyle(
            "BodyDarkBold",
            parent=body_style,
            fontName="Helvetica-Bold"
        )
        bullet_style = ParagraphStyle(
            "BulletText",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=COLOR_DARK_TEXT,
            leftIndent=14
        )
        disclaimer_style = ParagraphStyle(
            "Disclaimer",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=COLOR_MUTED
        )

        story = []

        # 1. Header Banner
        header_table = Table(
            [
                [
                    Paragraph("<b>MangoCare AI</b>", title_style),
                    Paragraph(f"<b>Report ID:</b> {analysis_id[:8]}...<br/><b>Date:</b> {datetime.now().strftime('%b %d, %Y %H:%M')}", subtitle_style)
                ],
                [
                    Paragraph("Automated Mango Health Assessment & Pathological Screening System", subtitle_style),
                    Paragraph("<b>Classification:</b> Educational Screening", subtitle_style)
                ]
            ],
            colWidths=[330, 202]
        )
        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=2, color=COLOR_PRIMARY, spaceAfter=12))

        # 2. Status & Key Assessment Summary Card
        status = analysis_data.get("status", "unknown")
        pred = analysis_data.get("prediction", {})
        cond_info = analysis_data.get("condition_information", {})

        status_text = "Suspected Disease Detected"
        status_color = COLOR_RED
        if status == "healthy_appearance_detected":
            status_text = "Healthy Appearance Detected"
            status_color = COLOR_SECONDARY
        elif status in ("inconclusive", "uncertain_result"):
            status_text = "Inconclusive / Uncertain Result"
            status_color = COLOR_AMBER

        pred_name = pred.get("class_name", "N/A")
        pred_conf = pred.get("confidence", 0.0)
        conf_cat = pred.get("confidence_category", "moderate").capitalize()
        sc_name = cond_info.get("scientific_name", "")

        summary_data = [
            [
                Paragraph("<b>Overall Status:</b>", body_style),
                Paragraph(f"<font color='{status_color.hexval()}'><b>{status_text}</b></font>", body_bold)
            ],
            [
                Paragraph("<b>Predicted Class:</b>", body_style),
                Paragraph(f"<b>{pred_name}</b> {f'<i>({sc_name})</i>' if sc_name else ''}", body_style)
            ],
            [
                Paragraph("<b>Model Confidence:</b>", body_style),
                Paragraph(f"{pred_conf:.1%} ({conf_cat} Confidence Score)", body_style)
            ],
            [
                Paragraph("<b>Interpretation:</b>", body_style),
                Paragraph(pred.get("confidence_interpretation", "N/A"), body_style)
            ]
        ]

        summary_table = Table(summary_data, colWidths=[130, 402])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOR_ACCENT_BG),
            ("BOX", (0, 0), (-1, -1), 1, COLOR_SECONDARY),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcfce7")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 12))

        # 3. Specimen Visual & Top Predictions Row
        story.append(Paragraph("Diagnostic Examination & Alternative Candidates", heading_style))

        # Embed thumbnail if bytes provided
        img_flowable = None
        if image_bytes:
            try:
                from PIL import Image
                pil_img = Image.open(io.BytesIO(image_bytes))
                thumb_bytes = create_safe_thumbnail_bytes(pil_img, max_dim=280)
                thumb_io = io.BytesIO(thumb_bytes)
                img_flowable = RLImage(thumb_io, width=1.9*inch, height=1.9*inch)
            except Exception as e:
                logger.warning(f"Could not prepare thumbnail for PDF: {e}")

        # Alternatives Table
        alt_list = analysis_data.get("alternatives", [])
        alt_rows = [[Paragraph("<b>Candidate Class</b>", body_bold), Paragraph("<b>Probability</b>", body_bold)]]
        # Include top prediction first
        alt_rows.append([Paragraph(f"1. {pred_name} (Top)", body_style), Paragraph(f"<b>{pred_conf:.1%}</b>", body_style)])
        for idx, alt in enumerate(alt_list, start=2):
            alt_rows.append([
                Paragraph(f"{idx}. {alt.get('class_name', 'N/A')}", body_style),
                Paragraph(f"{alt.get('confidence', 0.0):.1%}", body_style)
            ])

        alt_table = Table(alt_rows, colWidths=[200, 90])
        alt_table.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, 0), 1, COLOR_PRIMARY),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("BOX", (0, 0), (-1, -1), 1, COLOR_BORDER),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        if img_flowable:
            mid_table = Table(
                [[img_flowable, alt_table]],
                colWidths=[160, 372]
            )
            mid_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]))
            story.append(mid_table)
        else:
            story.append(alt_table)

        story.append(Spacer(1, 10))

        # 4. Visible Symptoms & Disease Profile
        symptoms = cond_info.get("visible_symptoms", [])
        if symptoms:
            story.append(Paragraph("Documented Visible Foliar Symptoms", heading_style))
            for sym in symptoms:
                story.append(Paragraph(f"• {sym}", bullet_style))
            story.append(Spacer(1, 8))

        # 5. Precautions & Recommended Actions
        story.append(Paragraph("Recommended Precautions & Integrated Management", heading_style))
        precautions = cond_info.get("prevention", [])
        for prec in precautions:
            story.append(Paragraph(f"• <b>Prevention:</b> {prec}", bullet_style))

        mgmt = cond_info.get("management_recommendations", [])
        for m in mgmt:
            story.append(Paragraph(f"• <b>Management:</b> {m}", bullet_style))

        story.append(Spacer(1, 10))

        # 6. Model & Technical Metadata Table
        story.append(Paragraph("Screening Model Provenance", heading_style))
        model_info = analysis_data.get("model", {})
        meta_table = Table(
            [
                [
                    Paragraph("<b>Vision Model:</b>", body_style),
                    Paragraph(f"{model_info.get('name', 'ixrbhii/mango-disease-convnext')}", body_style),
                    Paragraph("<b>Architecture:</b>", body_style),
                    Paragraph(f"{model_info.get('architecture', 'ConvNeXt-Small')}", body_style)
                ],
                [
                    Paragraph("<b>Screening Target:</b>", body_style),
                    Paragraph("Mango Foliage (Leaves)", body_style),
                    Paragraph("<b>Inference Mode:</b>", body_style),
                    Paragraph("CPU Evaluated (Local)", body_style)
                ]
            ],
            colWidths=[100, 166, 100, 166]
        )
        meta_table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 12))

        # 7. Regulatory Disclaimer
        story.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER, spaceAfter=8))
        disclaimer_p = (
            "<b>Important Agricultural Notice:</b> This automated diagnostic report is generated by a computer vision "
            "classification model designed for preliminary educational and screening use. It is NOT a laboratory-certified "
            "phytopathological confirmation. Environmental conditions, shadow effects, and foliar spray residues may alter visual "
            "features. Never apply restricted agrochemicals or high-dosage pesticides solely based on automated screening. "
            "For definitive diagnosis and regional treatment protocols, always consult your local agricultural extension service "
            "or an authorized crop protection specialist."
        )
        story.append(Paragraph(disclaimer_p, disclaimer_style))

        # Build document using NumberedCanvas
        doc.build(story, canvasmaker=NumberedCanvas)
        logger.info(f"Report generated successfully at {output_path}")
        return output_path

    def get_report_path(self, analysis_id: str) -> Optional[Path]:
        pdf_path = self.report_dir / f"MangoCare_Report_{analysis_id}.pdf"
        if pdf_path.is_file():
            return pdf_path
        return None
