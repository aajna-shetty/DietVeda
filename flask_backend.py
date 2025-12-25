from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from analytics import WellnessAnalytics
import sys
import os

# --- IMPORT YOUR MODULES ---
# This looks for the files in the same folder
try:
    from predictor import DietVedaAI
    from recommender import DietRecommender
    from yoga_coach import YogaCoach
    from routine_tracker import SattvaTracker
except ImportError as e:
    print("❌ CRITICAL ERROR: Missing Module.")
    print(f"Details: {e}")
    sys.exit()

# --- SETUP FLASK APP ---
app = Flask(__name__)
CORS(app)  # This is crucial! It allows React/Mobile to talk to Python.

# --- INITIALIZE ENGINES ONCE (At Startup) ---
print("🔄 Booting DietVeda Server...")
try:
    ai_brain = DietVedaAI()
    diet_engine = DietRecommender("dishes_dataset.csv")
    yoga_engine = YogaCoach()
    routine_engine = SattvaTracker()
    print("✅ All Engines Online & Ready to Serve.")
except Exception as e:
    print(f"❌ Initialization Failed: {e}")

# --- WEB ROUTES (HTML Templates) ---

@app.route('/')
def home():
    """Home dashboard"""
    return render_template('home.html')

@app.route('/dosha')
def dosha_diagnosis():
    """Dosha diagnosis page"""
    return render_template('dosha_diagnosis.html')

@app.route('/diet')
def diet_recommendations():
    """Diet recommendations page"""
    return render_template('diet_recommendations.html')

@app.route('/tongue')
def tongue_scanner():
    """Tongue scanner page"""
    return render_template('tongue_scanner.html')

@app.route('/routine')
def routine_tracker():
    """Routine tracker page"""
    return render_template('routine_tracker.html')

@app.route('/analytics')
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

@app.route('/yoga')
def yoga_coach():
    """Yoga coach page"""
    return render_template('yoga_coach.html')

@app.route('/chatbot')
def chatbot():
    """Dr. Veda chatbot page"""
    return render_template('chatbot.html')

# --- API ENDPOINTS (The "Menu" for your Frontend) ---

@app.route('/predict_dosha', methods=['POST'])
def predict_dosha():
    """
    Frontend sends: { "digestion": "fast", "sleep": "deep", ... }
    Backend replies: { "dosha": "Vata", "confidence": "85%" }
    """
    try:
        user_data = request.json
        result = ai_brain.predict(user_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_diet', methods=['POST'])
def get_diet():
    """
    Frontend sends: { "dosha": "Vata", "meal": "Lunch" }
    Backend replies: List of foods
    """
    try:
        data = request.json
        dosha = data.get('dosha')
        meal = data.get('meal')
        
        # Get recommendations from your existing engine
        recommendations = diet_engine.recommend(dosha, meal_type=meal)
        
        if recommendations.empty:
            return jsonify([])
        
        # Rename dish_type to meal_type for consistency in frontend
        if 'dish_type' in recommendations.columns:
            recommendations = recommendations.rename(columns={'dish_type': 'meal_type'})
        
        # Remove score column if it exists (we don't want to show scores)
        if 'score' in recommendations.columns:
            recommendations = recommendations.drop(columns=['score'])
        
        # Select only the columns we want to send to frontend
        columns_to_include = ['dish_name', 'ingredients', 'season', 'meal_type']
        # Add optional columns if they exist
        optional_columns = ['taste_profile', 'effect', 'dosha_suitable_for']
        for col in optional_columns:
            if col in recommendations.columns:
                columns_to_include.append(col)
        
        available_columns = [col for col in columns_to_include if col in recommendations.columns]
        recommendations = recommendations[available_columns]
        
        # Convert Pandas DataFrame to JSON
        return jsonify(recommendations.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_yoga', methods=['GET'])
def get_yoga():
    """
    Frontend asks: GET /get_yoga?dosha=Pitta
    Backend replies: List of videos
    """
    dosha = request.args.get('dosha')
    if not dosha:
        return jsonify({"error": "Dosha is required"}), 400

    primary_dosha = dosha.split("-")[0].capitalize()
    
    # Access the dictionary inside your YogaCoach class
    sequences = yoga_engine.sequences.get(primary_dosha, yoga_engine.sequences["Vata"])
    
    # Format nicely
    response = []
    for name, duration, url in sequences:
        response.append({
            "pose": name,
            "duration": duration,
            "url": url
        })
    return jsonify(response)

@app.route('/get_routine', methods=['GET'])
def get_routine():
    """
    Frontend asks: GET /get_routine?dosha=Vata
    Backend replies: List of habits
    """
    dosha = request.args.get('dosha')
    if not dosha:
        return jsonify({"error": "Dosha is required"}), 400
        
    primary_dosha = dosha.split("-")[0].capitalize()
    
    # Access data from RoutineTracker class
    specific = routine_engine.dosha_specific.get(primary_dosha, routine_engine.dosha_specific["Vata"])
    universal = routine_engine.universal_habits
    
    return jsonify({
        "universal": universal,
        "specific": specific
    })

@app.route('/analytics/graph')
def analytics_graph():
    """Generate and return progress graph"""
    try:
        wa = WellnessAnalytics()
        path = wa.generate_progress_graph(out_path="progress.png")
        if path and os.path.exists(path):
            return send_file(path, mimetype='image/png')
        # Fallback to existing file if generation fails
        if os.path.exists("progress.png"):
            return send_file("progress.png", mimetype='image/png')
        return jsonify({"error":"no-data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analytics/insights')
def analytics_insights():
    wa = WellnessAnalytics()
    return jsonify({"insights": wa.generate_insights()})

@app.route('/chat', methods=['POST'])
def chat():
    """
    Frontend sends: { "question": "Is curd good for dinner?", "dosha": "Vata" }
    Backend replies: { "response": "..." }
    """
    try:
        from chatbot import DrVedaChatbot
        bot = DrVedaChatbot()
        
        data = request.json
        question = data.get('question', '')
        dosha = data.get('dosha', 'Tridoshic')
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        response = bot.ask_dr_veda(question, dosha)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/full/<dosha>')
def download_full(dosha):
    """Download full diet chart PDF"""
    try:
        from diet_pdf import DietPDFGenerator
        generator = DietPDFGenerator("dishes_dataset.csv")
        path = generator.generate_full_chart(dosha, "full_chart.pdf")
        return send_file(path, as_attachment=True, download_name=f"dietveda_full_{dosha}.pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/filtered/<dosha>/<meal>')
def download_filtered(dosha, meal):
    """Download filtered meal PDF - uses same filtering as UI"""
    try:
        from diet_pdf import DietPDFGenerator
        import pandas as pd
        
        # Use the SAME filtering logic as the UI (recommend() method)
        # This ensures PDF contains only the foods shown in the UI
        meal_type = '' if meal.lower() == 'all' else meal
        recommendations = diet_engine.recommend(dosha, meal_type=meal_type)
        
        if recommendations.empty:
            return jsonify({"error": f"No dishes found for dosha: {dosha} and meal: {meal}"}), 404
        
        # Rename dish_type to meal_type for consistency
        if 'dish_type' in recommendations.columns:
            recommendations = recommendations.rename(columns={'dish_type': 'meal_type'})
        
        # Generate PDF with the filtered recommendations
        generator = DietPDFGenerator("dishes_dataset.csv")
        
        # Generate unique filename to avoid conflicts
        import time
        filename = f"filtered_{dosha.replace('-', '_')}_{meal}_{int(time.time())}.pdf"
        path = generator.generate_filtered_pdf(recommendations, dosha, meal, filename)
        
        if not os.path.exists(path):
            return jsonify({"error": "PDF generation failed"}), 500
            
        return send_file(path, as_attachment=True, download_name=f"dietveda_{dosha}_{meal}.pdf", mimetype='application/pdf')
    except Exception as e:
        import traceback
        print(f"PDF Error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


# --- START SERVER ---
if __name__ == '__main__':
    # Debug=True allows you to see errors in the console
    # Port 5000 is standard for Flask
    app.run(debug=True, port=5000)