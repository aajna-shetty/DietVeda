from flask import Flask, request, jsonify
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

# --- API ENDPOINTS (The "Menu" for your Frontend) ---

@app.route('/')
def home():
    """Simple check to see if server is running"""
    return jsonify({
        "status": "Online", 
        "project": "DietVeda AI", 
        "version": "1.0"
    })

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
    wa = WellnessAnalytics()
    path = wa.generate_progress_graph(out_path="progress.png")
    if path and os.path.exists(path):
        return send_file(path, mimetype='image/png')
    return jsonify({"error":"no-data"}), 404

@app.route('/analytics/insights')
def analytics_insights():
    wa = WellnessAnalytics()
    return jsonify({"insights": wa.generate_insights()})


# --- START SERVER ---
if __name__ == '__main__':
    # Debug=True allows you to see errors in the console
    # Port 5000 is standard for Flask
    app.run(debug=True, port=5000)