# app.py
import sys
import time
import os

# --- IMPORTING YOUR MODULES ---
try:
    from predictor import DietVedaAI
    from recommender import DietRecommender
    from yoga_coach import YogaCoach
    from tongue_scanner import LiveTongueScanner
    from routine_tracker import SattvaTracker
    from analytics import WellnessAnalytics
except ImportError as e:
    print("❌ CRITICAL ERROR: Missing Module.")
    print(f"Details: {e}")
    sys.exit()

# --- HELPER FUNCTIONS ---
def typing_effect(text, delay=0.008):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_enter():
    input("\nPress Enter to continue...")

# ---------------------------------------------------------
#                      MAIN APP
# ---------------------------------------------------------
def main():
    clear_screen()
    typing_effect("🔄 Booting DietVeda Core Systems...")

    # Initialize Engines
    try:
        ai_brain = DietVedaAI()
        diet_engine = DietRecommender("dishes_dataset.csv")
        yoga_engine = YogaCoach()
        scanner_engine = LiveTongueScanner()
        routine_engine = SattvaTracker()
        print("✅ All Modules Loaded Successfully.")
    except Exception as e:
        print(f"❌ Initialization Failed: {e}")
        return

    time.sleep(0.5)
    clear_screen()

    print("=" * 60)
    print("🌿  D I E T V E D A   I N T E L L I G E N C E  🌿")
    print("=" * 60)

    # ---------------------------------------------------------
    #                PHASE 1: IDENTIFICATION
    # ---------------------------------------------------------
    print("\n[1] New Analysis (Take Quiz)")
    print("[2] I Know My Dosha (Manual Entry)")

    start_choice = input("\nSelect Option (1-2): ").strip()
    user_dosha = "Vata"  # fallback default

    # --------------------- QUIZ MODE -------------------------
    if start_choice == "1":
        typing_effect("\n📝 Analyzing Bio-Constitution...")

        profile = {
            'digestion': input("   Digestion (fast/slow/moderate): ").strip().lower(),
            'sleep': input("   Sleep (light/deep/moderate): ").strip().lower(),
            'energy': input("   Energy (low/high/moderate): ").strip().lower(),
            'temperature_preference': input("   Temp Pref (cold/warm/moderate): ").strip().lower(),
            'mood': input("   Mood (anxious/calm/irritable): ").strip().lower(),
            'body_frame': input("   Body Frame (slim/broad/medium): ").strip().lower()
        }

        print("\n🧠 Processing...")
        result = ai_brain.predict(profile)

        if isinstance(result, dict) and "error" in result:
            print(f"❌ Error: {result['error']}")
            return

        user_dosha = result.get('dosha', 'Vata')
        typing_effect(f"✨ DIAGNOSIS COMPLETE: You are {result.get('type','')} - {user_dosha.upper()}")
        print(f"   (Confidence: {result.get('confidence','N/A')})")

    # -------------------- MANUAL ENTRY -----------------------
    else:
        print("\n🌿 Enter your dominant dosha manually.")

        valid_doshas = [
            "vata", "pitta", "kapha",
            "vata-pitta", "pitta-vata",
            "pitta-kapha", "kapha-pitta",
            "vata-kapha", "kapha-vata"
        ]

        while True:
            user_dosha = input(
                "Dosha (Vata / Pitta / Kapha or dual like Vata-Pitta): "
            ).strip().lower()

            if user_dosha in valid_doshas:
                break
            else:
                print("❌ Invalid dosha. Try again.\n")

        # Format only for display
        user_dosha = user_dosha.capitalize()
        print(f"\n✔ Using Dosha: {user_dosha}")

    prompt_enter()

    # ---------------------------------------------------------
    #                PHASE 2: DASHBOARD
    # ---------------------------------------------------------
    while True:
        clear_screen()
        season = diet_engine._get_season() if hasattr(diet_engine, "_get_season") else "Unknown"

        print(f"👤 USER: {user_dosha.upper()} | 📅 SEASON: {season}")
        print("-" * 60)
        print("1. 🥗 Get Diet Recommendations")
        print("2. 🧘 Video Yoga Coach")
        print("3. 📅 Sattva Routine Tracker")
        print("4. 📸 Live Tongue Scanner (Computer Vision)")
        print("5. 📈 Wellness Progress Analytics (Last 30 Days)")
        print("6. 🤖 Chat with Dr. Veda (AI)")
        print("7. ❌ Exit")
        print("-" * 60)

        choice = input("Select Feature (1-7): ").strip()

        # ---------------------------------------------------------
        # 1. Diet Recommendations
        # ---------------------------------------------------------
        if choice == "1":
            print("\n🥗 DIET PLAN")
            meal = input("Which meal? (Breakfast/Lunch/Dinner — leave blank for All): ").strip()

            recs = diet_engine.recommend(user_dosha, meal)

            if recs.empty:
                print("No matches found.")
            else:
                print(recs[['dish_name', 'score', 'ingredients']].to_string(index=False))

            print("\n[1] Continue")
            print("[2] Download Full Food Chart")
            print("[3] Download Filtered Meal PDF")
            print("[4] Back to Dashboard")

            sub = input("Choose (1-4): ")

            from diet_pdf import DietPDFGenerator
            gen = DietPDFGenerator("dishes_dataset.csv")

            if sub == "2":
                path = gen.generate_full_chart(user_dosha)
                print(f"📄 Full diet chart saved as: {path}")

            elif sub == "3":
                path = gen.generate_filtered_pdf(recs, user_dosha, meal or "All")
                print(f"📄 Filtered meal PDF saved as: {path}")

            prompt_enter()

        # ---------------------------------------------------------
        # 2. Yoga Coach
        # ---------------------------------------------------------
        elif choice == "2":
            yoga_engine.start_session(user_dosha)
            prompt_enter()

        # ---------------------------------------------------------
        # 3. Routine Tracker
        # ---------------------------------------------------------
        elif choice == "3":
            routine_engine.start_tracking(user_dosha)
            prompt_enter()

        # ---------------------------------------------------------
        # 4. Tongue Scanner
        # ---------------------------------------------------------
        elif choice == "4":
            scanner_engine.start_scanning()
            prompt_enter()

        # ---------------------------------------------------------
        # 5. Wellness Analytics
        # ---------------------------------------------------------
        elif choice == "5":
            wa = WellnessAnalytics()
            out = wa.generate_progress_graph(out_path="progress.png")
            print()
            print(wa.generate_insights())
            if out:
                print(f"📁 Graph saved as: {out}")
            prompt_enter()

        # ---------------------------------------------------------
        # 6. Dr. Veda Chatbot
        # ---------------------------------------------------------
        elif choice == "6":
            from chatbot import DrVedaChatbot
            bot = DrVedaChatbot()

            clear_screen()
            print(f"\n🤖 DR. VEDA AI ({user_dosha.upper()} Specialist)")
            print("Type 'exit' to go back.")
            print("-" * 50)

            while True:
                user_q = input("\n👤 You: ").strip()
                if user_q.lower() in ("exit", "quit", "back"):
                    print("\nEnding Chat Session...")
                    time.sleep(1)
                    break

                print("...Thinking...")
                ai_response = bot.ask_dr_veda(user_q, user_dosha)

                print(f"\n🌿 Dr. Veda: {ai_response}\n")

            prompt_enter()

        # ---------------------------------------------------------
        # 7. Exit
        # ---------------------------------------------------------
        elif choice == "7":
            typing_effect("\n🌿 Shutting down. Live Balanced. 🌿")
            break

        else:
            print("Invalid choice.")
            time.sleep(1)


if __name__ == "__main__":
    main()