class LifestyleModule:
    def __init__(self):
        # HARDCODED KNOWLEDGE BASE (Expert System)
        # In a real startup, this would be a database.
        
        self.yoga_db = {
            "Vata": {
                "focus": "Grounding & Calming",
                "poses": [
                    {"name": "Vrikshasana (Tree Pose)", "benefit": "Improves balance and focus, grounding excess air."},
                    {"name": "Paschimottanasana (Seated Forward Bend)", "benefit": "Calms the nervous system."},
                    {"name": "Balasana (Child's Pose)", "benefit": "Relieves anxiety and mental stress."}
                ],
                "tip": "Focus on slow, steady movements. Avoid jumping."
            },
            "Pitta": {
                "focus": "Cooling & Relaxing",
                "poses": [
                    {"name": "Chandra Namaskar (Moon Salutation)", "benefit": "Cooling energy, removes body heat."},
                    {"name": "Bhujangasana (Cobra Pose)", "benefit": "Releases tension in the abdomen without overheating."},
                    {"name": "Shavasana (Corpse Pose)", "benefit": "Essential for cooling the fire element."}
                ],
                "tip": "Avoid hot yoga or excessive sweating. Practice in the evening."
            },
            "Kapha": {
                "focus": "Stimulating & Energizing",
                "poses": [
                    {"name": "Surya Namaskar (Sun Salutation)", "benefit": "Builds heat and burns stagnation."},
                    {"name": "Virabhadrasana (Warrior Pose)", "benefit": "Increases metabolism and heart rate."},
                    {"name": "Dhanurasana (Bow Pose)", "benefit": "Stimulates digestion and removes lethargy."}
                ],
                "tip": "Move quickly. Hold poses for shorter durations but repeat often."
            }
        }

        self.routine_db = {
            "Vata": [
                ("06:00 AM", "Wake up. Drink warm water with lemon."),
                ("07:00 AM", "Oil massage (Abhyanga) with Sesame oil."),
                ("10:00 PM", "Strict bedtime. Vata needs the most sleep.")
            ],
            "Pitta": [
                ("05:30 AM", "Wake up. Cool water splash on eyes."),
                ("07:00 AM", "Exercise/Yoga during the coolest part of the day."),
                ("11:00 PM", "Bedtime. Do not work late at night (Fire time).")
            ],
            "Kapha": [
                ("05:00 AM", "Wake up before sunrise (Brahma Muhurta)."),
                ("06:30 AM", "Vigorous exercise (Cardio/Run) to break stagnation."),
                ("10:00 PM", "Bedtime. Avoid sleeping during the day.")
            ]
        }

    def get_yoga(self, dosha):
        # Handle Dual Doshas simply (Prioritize primary)
        primary = dosha.split("-")[0] 
        return self.yoga_db.get(primary, self.yoga_db['Vata'])

    def get_routine(self, dosha):
        primary = dosha.split("-")[0]
        return self.routine_db.get(primary, self.routine_db['Vata'])