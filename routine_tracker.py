import time
import sys
from progress_db import ProgressDB

class SattvaTracker:
    def __init__(self):
        self.db = ProgressDB()

        self.universal_habits = [
            ("Wake up before 6:00 AM (Brahma Muhurta)", 20),
            ("Tongue Scraping (Jivha Prakshalana)", 10),
            ("Drink Warm Copper Water", 10),
            ("No Screen Time 1hr before Bed", 15)
        ]
        
        self.dosha_specific = {
            "Vata": [
                ("Self-Massage with Sesame Oil (Abhyanga)", 20),
                ("Eat a warm, cooked breakfast", 15),
                ("Bedtime by 10:00 PM", 20)
            ],
            "Pitta": [
                ("Cool shower or swim", 15),
                ("Avoid spicy/fried foods today", 20),
                ("Meditation for 10 mins", 20)
            ],
            "Kapha": [
                ("Dry Brushing (Garshana)", 15),
                ("Vigorous Exercise (Sweat it out)", 25),
                ("No napping during the day", 15)
            ]
        }

    def start_tracking(self, dosha):
        # Handle dual dosha
        primary_dosha = dosha.split("-")[0].capitalize()

        my_habits = self.dosha_specific.get(primary_dosha, self.dosha_specific["Vata"])
        full_checklist = self.universal_habits + my_habits

        print(f"\n📅 SATTVA ROUTINE TRACKER FOR {primary_dosha.upper()}")
        print("Let's calculate your 'Purity Score' for today.")
        print("-" * 50)
        time.sleep(1)

        total_score = 0
        max_possible = sum([p for _, p in full_checklist])

        # Ask questions once (✔ FIXED)
        for habit, points in full_checklist:
            ans = input(f"Did you do: '{habit}'? (y/n): ").strip().lower()
            if ans == 'y':
                print(f"   ✅ Excellent! (+{points} pts)")
                total_score += points
            else:
                print(f"   ❌ Missed it. (0 pts)")
            time.sleep(0.2)

        percentage = int((total_score / max_possible) * 100)

        # Save once (✔ FIXED)
        self.db.save_score(primary_dosha, percentage)
        print("📊 Daily score saved to your wellness history!")

        print("-" * 50)
        print(f"🏆 TOTAL SCORE: {total_score} / {max_possible} ({percentage}%)")

        # Gamification
        if percentage >= 90:
            print("🌟 RANK: AYURVEDIC YOGI (Perfect Balance!)")
        elif percentage >= 70:
            print("🌿 RANK: DISCIPLINED SEEKER (Great job!)")
        elif percentage >= 50:
            print("🌱 RANK: BEGINNER (Good start, keep trying!)")
        else:
            print("⚠️ RANK: OUT OF BALANCE (Needs attention tomorrow)")

        print("-" * 50)


# --- TEST ---
if __name__ == "__main__":
    tracker = SattvaTracker()
    tracker.start_tracking("Vata")
