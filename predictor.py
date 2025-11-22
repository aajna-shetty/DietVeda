import pandas as pd
import joblib
import numpy as np

class DietVedaAI:
    def __init__(self):
        # Load the pre-trained brain
        try:
            self.model = joblib.load('dietveda_complex_model.pkl')
            self.encoders = joblib.load('dietveda_encoders.pkl')
            self.dosha_classes = self.encoders['dosha'].classes_
        except FileNotFoundError:
            raise Exception("❌ Model not found! Run train_brain.py first.")

    def predict(self, user_profile):
        """
        Complex Prediction Logic:
        Returns not just the Dosha, but the Probability Distribution
        to detect 'Dual Doshas' (e.g., Vata-Pitta).
        """
        # 1. Preprocess Input
        processed_input = {}
        try:
            for feature, value in user_profile.items():
                encoder = self.encoders[feature]
                # Handle unseen labels safely
                if value not in encoder.classes_:
                    raise ValueError(f"Unknown value '{value}' for {feature}")
                processed_input[feature] = [encoder.transform([value])[0]]
        except ValueError as e:
            return {"error": str(e)}

        # 2. Get Probabilities (The Complex Part)
        # Instead of simple .predict(), we use .predict_proba()
        # Output example: [0.1, 0.6, 0.3] (10% Kapha, 60% Pitta, 30% Vata)
        input_df = pd.DataFrame(processed_input)
        probs = self.model.predict_proba(input_df)[0]
        
        # Map probabilities to Dosha names
        dosha_probs = dict(zip(self.dosha_classes, probs))
        
        # 3. Analyze for Dual Dosha (Advanced Logic)
        # Sort doshas by score
        sorted_doshas = sorted(dosha_probs.items(), key=lambda item: item[1], reverse=True)
        
        primary_dosha = sorted_doshas[0]   # e.g., ('Vata', 0.55)
        secondary_dosha = sorted_doshas[1] # e.g., ('Pitta', 0.40)
        
        # If the gap between 1st and 2nd is small (< 15%), it's a Dual Dosha
        if (primary_dosha[1] - secondary_dosha[1]) < 0.15:
            prediction_type = "Dual Dosha"
            final_dosha = f"{primary_dosha[0]}-{secondary_dosha[0]}"
        else:
            prediction_type = "Single Dosha"
            final_dosha = primary_dosha[0]

        return {
            "type": prediction_type,
            "dosha": final_dosha,
            "confidence": f"{int(primary_dosha[1] * 100)}%",
            "breakdown": dosha_probs # Optional: Show pie chart data
        }

# --- USER INTERFACE (Simulated) ---
def run_app():
    print("\n🍃 --- DIETVEDA INTELLIGENT SYSTEM --- 🍃")
    print("Please answer the following to analyze your body constitution.\n")
    
    # Questions mapped to dataset columns
    q_map = {
        'digestion': "Digestion (fast/slow/moderate): ",
        'sleep': "Sleep Quality (light/deep/moderate): ",
        'energy': "Energy Level (low/moderate/high): ",
        'temperature_preference': "Temp Preference (cold/warm/moderate): ",
        'mood': "Mood (anxious/calm/irritable/enthusiastic): ",
        'body_frame': "Body Frame (slim/broad/medium): "
    }
    
    user_input = {}
    for key, question in q_map.items():
        user_input[key] = input(question).lower().strip()

    # Run Analysis
    ai = DietVedaAI()
    result = ai.predict(user_input)

    if "error" in result:
        print(f"\n⚠️ {result['error']}")
    else:
        print("\n" + "="*30)
        print(f"🔮 ANALYSIS COMPLETE")
        print(f"TYPE: {result['type']}")
        print(f"DOSHA: {result['dosha']}")
        print(f"CONFIDENCE: {result['confidence']}")
        print("="*30)
        
        # Explanation
        if result['type'] == "Dual Dosha":
            print(f"💡 Note: You have a complex constitution. You show strong traits of both.")
            print("Your diet should balance both doshas.")
        else:
            print(f"💡 Note: You have a clear dominant constitution.")

# Run the app
if __name__ == "__main__":
    run_app()