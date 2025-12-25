# chatbot.py
import google.generativeai as genai
import os

class DrVedaChatbot:
    def __init__(self):
        
        self.api_key = "API-KEY"

        self.is_active = False

        try:
            genai.configure(api_key=self.api_key)

          
            self.model = genai.GenerativeModel("gemini-2.0-flash")

            self.is_active = True
            print("✅ Connected to Gemini API (model: gemini-2.0-flash)")
        except Exception as e:
            print(f"❌ Gemini API Setup Failed: {e}")
            self.is_active = False

    def ask_dr_veda(self, question, dosha="Tridoshic"):
        """
        Sends the question to Gemini with the Ayurvedic persona prompt.
        """

        if not self.is_active:
            return "❌ Dr. Veda is offline. Please check your Gemini API key."

        
        prompt = f"""
        You are Dr. Veda — an Ayurvedic physician with 20+ years experience.

        The user has DOSHA: {dosha.upper()}.

        Answer the question below in:
        • 2–3 short sentences  
        • simple and comforting tone  
        • Ayurvedic accuracy  
        • include 1–2 food or lifestyle tips specifically for {dosha}  

        USER QUESTION: "{question}"
        """

        try:
            response = self.model.generate_content(prompt)

            if response and response.text:
                return response.text.strip()

            return "🧘‍♂️ I am reflecting... please ask again."
        except Exception as e:
            return f"⚠️ API Error: {e}"


# QUICK TEST
if __name__ == "__main__":
    print("🔍 Testing Dr. Veda Chatbot...\n")

    bot = DrVedaChatbot()

    if bot.is_active:
        ans = bot.ask_dr_veda("Is curd good for dinner?", "Vata")
        print("\n🤖 Dr. Veda says:\n", ans)
    else:
        print("❌ Chatbot could not be started.")
