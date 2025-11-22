import time
import sys
import webbrowser # <--- The new magic tool

class YogaCoach:
    def __init__(self):
        # Database: Pose Name, Duration, and YouTube Link
        self.sequences = {
            "Vata": [
                ("Child's Pose", 60, "https://www.youtube.com/watch?v=eqVMAPM00DM"), 
                ("Tree Pose", 30, "https://www.youtube.com/watch?v=wdln9qWYloU"), 
                ("Corpse Pose", 120, "https://www.youtube.com/watch?v=Mc-38vuwE1Y")
            ],
            "Pitta": [
                ("Moon Salutation", 60, "https://www.youtube.com/watch?v=0RBUP1b87Tk"), 
                ("Cobra Pose", 30, "https://www.youtube.com/watch?v=fOdrW7nf9gw")
            ],
            "Kapha": [
                ("Sun Salutation", 30, "https://www.youtube.com/watch?v=1xRX1MuoImw"), 
                ("Warrior II", 30, "https://www.youtube.com/watch?v=DoC5mh9GxF4")
            ]
        }

    def start_session(self, dosha):
        primary_dosha = dosha.split("-")[0]
        sequence = self.sequences.get(primary_dosha, self.sequences["Vata"])
        
        print(f"\n🧘 STARTING {primary_dosha.upper()} YOGA SESSION")
        print("Prepare your mat. The video guide will open automatically.")
        time.sleep(2)
        
        for pose_name, duration, video_url in sequence:
            print("\n" + "="*40)
            print(f"👉 NEXT POSE: {pose_name}")
            print(f"   Opening video guide...")
            
            # --- AUTO-OPEN BROWSER ---
            webbrowser.open(video_url)
            # -------------------------
            
            print(f"   Hold this pose for {duration} seconds.")
            print("   (Switch back to this window to see timer)")
            
            # Countdown Timer
            for i in range(duration, 0, -1):
                sys.stdout.write(f"\r⏳ {i}s remaining... ")
                sys.stdout.flush()
                time.sleep(1) 
            
            print("\r✅ Release! Relax for 5s...                    ")
            time.sleep(5)
            
        print("\n✨ NAMASTE. Session Complete.")