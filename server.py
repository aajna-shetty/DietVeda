# server.py
from flask import Flask, send_from_directory, jsonify
from diet_pdf import DietPDFGenerator
import os
import pandas as pd

app = Flask(__name__)

PDF_DIR = "DietVeda_Reports"
os.makedirs(PDF_DIR, exist_ok=True)

generator = DietPDFGenerator("dishes_dataset.csv")

# -----------------------------
# FULL CHART DOWNLOAD
# -----------------------------
@app.route("/download/full/<dosha>")
def download_full(dosha):
    try:
        path = generator.generate_full_chart(dosha, "full_chart.pdf")
        return send_from_directory(PDF_DIR, "full_chart.pdf", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# FILTERED MEAL DOWNLOAD
# -----------------------------
@app.route("/download/filtered/<dosha>/<meal>")
def download_filtered(dosha, meal):
    try:
        # Frontend must send meal name like Lunch / Dinner
        df = generator.filter_by_dosha(dosha)
        df = df[df['meal_type'].str.lower() == meal.lower()]  # meal must exist in your CSV

        if df.empty:
            return jsonify({"error": "No dishes found"}), 404

        path = generator.generate_filtered_pdf(df, dosha, meal, "filtered_chart.pdf")
        return send_from_directory(PDF_DIR, "filtered_chart.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "DietVeda PDF Server Running!"


if __name__ == "__main__":
    app.run(debug=True)
