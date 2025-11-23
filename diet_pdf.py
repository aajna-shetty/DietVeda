# diet_pdf.py
import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


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
        return self.df[self.df["dosha_suitable_for"]
                       .str.lower()
                       .str.contains(dosha)]

    # ---------------------------------------------------------
    # FULL FOOD CHART — PREMIUM CARD DESIGN
    # ---------------------------------------------------------
    def generate_full_chart(self, dosha, out_path="full_diet_chart.pdf"):

        data = self.filter_by_dosha(dosha)
        if data.empty:
            raise ValueError("No dishes found for this dosha.")

        # Save inside folder
        out_path = os.path.join(DOWNLOAD_DIR, out_path)

        pdf = SimpleDocTemplate(out_path, pagesize=letter)
        story = []

        # Title
        title = f"Diet Chart for {dosha.capitalize()} Dosha"
        story.append(Paragraph(f"<b>{title}</b>", self.styles["Title"]))
        story.append(Spacer(1, 20))

        # Card background color
        card_color = "#E9F7EF"

        # Create card blocks
        for _, row in data.iterrows():

            block = f"""
            <para backColor="{card_color}" 
                  spaceBefore="10" spaceAfter="10"
                  leftIndent="8" rightIndent="8">

                <font size=14><b>{row['dish_name']}</b></font><br/><br/>

                <font size=10>
                <b>Ingredients:</b> {row['ingredients']}<br/><br/>

                <b>Suitable For:</b> {row['dosha_suitable_for']}<br/>
                <b>Avoids For:</b> {row['avoids_for']}<br/><br/>

                <b>Taste Profile:</b> {row['taste_profile']}<br/>
                <b>Effect:</b> {row['effect']}<br/>
                <b>Season:</b> {row['season']}<br/>
                </font>

            </para>
            """

            story.append(Paragraph(block, self.styles["BodyText"]))
            story.append(Spacer(1, 12))

        pdf.build(story)

        # Auto-open folder (Windows)
        try:
            os.startfile(os.path.dirname(out_path))
        except:
            pass

        return os.path.abspath(out_path)

    # ---------------------------------------------------------
    # FILTERED MEAL PDF — TABLE FORMAT
    # ---------------------------------------------------------
    def generate_filtered_pdf(self, df, dosha, meal, out_path="filtered_meal.pdf"):

        if df.empty:
            raise ValueError("No filtered dishes to export.")

        # Save inside folder
        out_path = os.path.join(DOWNLOAD_DIR, out_path)

        pdf = SimpleDocTemplate(out_path, pagesize=letter)
        story = []

        title = f"{meal} Recommendations for {dosha.capitalize()} Dosha"
        story.append(Paragraph(f"<b>{title}</b>", self.styles["Title"]))
        story.append(Spacer(1, 20))

        # Table header
        table_data = [["Dish Name", "Ingredients", "Score"]]

        # Add all rows
        for _, row in df.iterrows():
            table_data.append([
                row["dish_name"],
                row["ingredients"],
                str(row["score"])
            ])

        # Table design
        table = Table(table_data, colWidths=[150, 300, 50])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#cfe8ff")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),

            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),

            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        story.append(table)
        pdf.build(story)

        # Auto-open folder
        try:
            os.startfile(os.path.dirname(out_path))
        except:
            pass

        return os.path.abspath(out_path)
