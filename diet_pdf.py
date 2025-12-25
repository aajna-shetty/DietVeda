# diet_pdf.py
import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


# ---------------------------------------------------------
# CREATE DOWNLOAD DIRECTORY
# ---------------------------------------------------------
DOWNLOAD_DIR = "DietVeda_Reports"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class DietPDFGenerator:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.styles = getSampleStyleSheet()

    # ---------------------------------------------------------
    # FILTER BY DOSHA
    # ---------------------------------------------------------
    def filter_by_dosha(self, dosha):
        dosha = dosha.lower()
        
        # Handle dual doshas (e.g., "Pitta-Vata" or "Vata-Pitta")
        if "-" in dosha:
            doshas = [d.strip() for d in dosha.split("-")]
            # Create a mask that matches if dish is suitable for ANY of the doshas
            mask = self.df["dosha_suitable_for"].str.lower().str.contains(doshas[0], na=False)
            for d in doshas[1:]:
                mask = mask | self.df["dosha_suitable_for"].str.lower().str.contains(d, na=False)
            return self.df[mask]
        else:
            # Single dosha - simple contains check
            return self.df[self.df["dosha_suitable_for"]
                           .str.lower()
                           .str.contains(dosha, na=False)]

    # ---------------------------------------------------------
    # MANDALA HEADER FUNCTION
    # ---------------------------------------------------------
    def _draw_mandala_header(self, canvas, doc):
        """Draw mandala-inspired header on each page"""
        canvas.saveState()
        # Mandala circle (simplified)
        canvas.setStrokeColor(colors.HexColor("#B87333"))  # Copper
        canvas.setLineWidth(2)
        canvas.circle(4.25*inch, 10.5*inch, 0.3*inch, stroke=1, fill=0)
        canvas.circle(4.25*inch, 10.5*inch, 0.2*inch, stroke=1, fill=0)
        
        # Title with Ayurvedic styling
        canvas.setFont("Helvetica-Bold", 20)
        canvas.setFillColor(colors.HexColor("#6B8E6B"))  # Herbal green
        canvas.drawString(1*inch, 10.7*inch, "🌿 DietVeda 🌿")
        
        canvas.restoreState()

    # ---------------------------------------------------------
    # FULL FOOD CHART — PREMIUM CARD DESIGN
    # ---------------------------------------------------------
    def generate_full_chart(self, dosha, out_path="full_diet_chart.pdf"):

        data = self.filter_by_dosha(dosha)
        if data.empty:
            raise ValueError("No dishes found for this dosha.")

        # Save inside folder
        out_path = os.path.join(DOWNLOAD_DIR, out_path)

        pdf = SimpleDocTemplate(out_path, pagesize=letter, 
                                onFirstPage=self._draw_mandala_header,
                                onLaterPages=self._draw_mandala_header)
        story = []

        # Title with Ayurvedic quote
        title_style = ParagraphStyle(
            'AyurvedicTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor("#6B8E6B"),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        title = f"<b>🌿 Diet Chart for {dosha.capitalize()} Dosha 🌿</b>"
        story.append(Paragraph(title, title_style))
        
        quote = "<i>\"Balance is the essence of health — Sushruta Samhita\"</i>"
        story.append(Paragraph(quote, self.styles["Normal"]))
        story.append(Spacer(1, 30))

        # Card background color (soft pastel green)
        card_color = "#E9F7EF"
        border_color = "#B87333"  # Copper

        # Create card blocks with enhanced styling
        card_style = ParagraphStyle(
            'FoodCard',
            parent=self.styles['BodyText'],
            backColor=colors.HexColor(card_color),
            borderColor=colors.HexColor(border_color),
            borderWidth=2,
            borderPadding=12,
            leftIndent=12,
            rightIndent=12,
            spaceBefore=15,
            spaceAfter=15
        )
        
        for _, row in data.iterrows():
            dish_name = row.get('dish_name', 'Unknown Dish')
            ingredients = row.get('ingredients', 'N/A')
            suitable = row.get('dosha_suitable_for', 'N/A')
            avoids = row.get('avoids_for', 'N/A')
            taste = row.get('taste_profile', 'N/A')
            effect = row.get('effect', 'N/A')
            season = row.get('season', 'N/A')

            block = f"""
            <para>
                <font size=16 color="#6B8E6B"><b>🌿 {dish_name}</b></font><br/><br/>

                <font size=11 color="#3D2817">
                <b>Ingredients:</b> {ingredients}<br/><br/>

                <b>Suitable For:</b> <font color="#6B8E6B">{suitable}</font><br/>
                <b>Avoids For:</b> {avoids}<br/><br/>

                <b>Taste Profile:</b> {taste}<br/>
                <b>Effect:</b> {effect}<br/>
                <b>Season:</b> {season}<br/>
                </font>
            </para>
            """

            story.append(Paragraph(block, card_style))
            story.append(Spacer(1, 15))

        pdf.build(story)

        # Auto-open folder (Windows)
        try:
            os.startfile(os.path.dirname(out_path))
        except:
            pass

        return os.path.abspath(out_path)

    # ---------------------------------------------------------
    # FILTERED MEAL PDF — TABLE FORMAT WITH AYURVEDIC STYLING
    # ---------------------------------------------------------
    def generate_filtered_pdf(self, df, dosha, meal, out_path="filtered_meal.pdf"):
        """
        Generate PDF from a pre-filtered DataFrame (from recommend() method)
        This ensures PDF matches what's shown in the UI
        """
        if df.empty:
            raise ValueError("No filtered dishes to export.")

        # Save inside folder
        out_path = os.path.join(DOWNLOAD_DIR, out_path)

        pdf = SimpleDocTemplate(out_path, pagesize=letter,
                                onFirstPage=self._draw_mandala_header,
                                onLaterPages=self._draw_mandala_header)
        story = []

        # Enhanced title
        title_style = ParagraphStyle(
            'MealTitle',
            parent=self.styles['Title'],
            fontSize=22,
            textColor=colors.HexColor("#6B8E6B"),
            spaceAfter=20,
            alignment=1
        )
        
        title = f"<b>🥗 {meal} Recommendations for {dosha.capitalize()} Dosha 🥗</b>"
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 25))

        # Table header (removed Score column)
        table_data = [["Dish Name", "Ingredients", "Season"]]

        # Add all rows
        for _, row in df.iterrows():
            table_data.append([
                row.get("dish_name", "Unknown"),
                row.get("ingredients", "N/A"),
                row.get("season", "All")
            ])

        # Table design with Ayurvedic colors
        table = Table(table_data, colWidths=[200, 350, 100])

        table.setStyle(TableStyle([
            # Header row
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6B8E6B")),  # Herbal green
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            
            # Data rows - alternating colors
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#E9F7EF")),  # Soft green
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#3D2817")),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),

            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Borders with copper color
            ("GRID", (0, 0), (-1, -1), 1.5, colors.HexColor("#B87333")),  # Copper
            ("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#B87333")),

            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            
            # Row striping
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#E9F7EF"), colors.white]),
        ]))

        story.append(table)
        pdf.build(story)

        # Auto-open folder
        try:
            os.startfile(os.path.dirname(out_path))
        except:
            pass

        return os.path.abspath(out_path)
