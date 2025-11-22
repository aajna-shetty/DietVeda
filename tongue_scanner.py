import cv2
import numpy as np

class LiveTongueScanner:
    def start_scanning(self):
        print("📸 STARTING WEBCAM... (Press 'q' to Quit)")
        
        # 1. Open Webcam (0 is usually the default camera)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open webcam.")
            return

        while True:
            # 2. Read a frame from the camera
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally (mirror effect) so it feels natural
            frame = cv2.flip(frame, 1)
            
            # 3. Define the "Target Box" (Region of Interest)
            # We want a box in the center of the screen
            height, width, _ = frame.shape
            box_size = 200
            x = (width - box_size) // 2
            y = (height - box_size) // 2
            
            # Draw the rectangle (Green box)
            cv2.rectangle(frame, (x, y), (x + box_size, y + box_size), (0, 255, 0), 2)
            cv2.putText(frame, "PLACE TONGUE HERE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # 4. Crop the box to analyze only the tongue
            roi = frame[y:y+box_size, x:x+box_size]
            
            # 5. Analyze Color (Average BGR)
            # OpenCV uses BGR format, not RGB
            avg_color_per_row = np.average(roi, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            
            blue = int(avg_color[0])
            green = int(avg_color[1])
            red = int(avg_color[2])
            
            # 6. Diagnosis Logic (Simple Color Thresholding)
            diagnosis = "Analyzing..."
            color = (255, 255, 255) # Default Text Color
            
            # Logic:
            # - High Red + Low Green/Blue = Pitta (Inflammation)
            # - High Green/Blue/Red (All high) = White Coating (Ama/Toxins)
            # - Balanced Red/Pink = Healthy
            
            if red > 160 and green < 120 and blue < 120:
                diagnosis = "High Pitta (Redness Detected)"
                color = (0, 0, 255) # Red Text
            elif red > 180 and green > 180 and blue > 180:
                diagnosis = "Ama / Toxins (White Coating)"
                color = (200, 200, 200) # Grey Text
            elif red > 130 and green < 140:
                diagnosis = "Healthy (Pink)"
                color = (0, 255, 0) # Green Text
            else:
                diagnosis = "Adjust Lighting..."
            
            # 7. Display Diagnosis on Screen
            cv2.putText(frame, f"Diagnosis: {diagnosis}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, f"R:{red} G:{green} B:{blue}", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # 8. Show the Window
            cv2.imshow('DietVeda Live Scanner', frame)
            
            # Quit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()

# --- Test it independently ---
if __name__ == "__main__":
    scanner = LiveTongueScanner()
    scanner.start_scanning()