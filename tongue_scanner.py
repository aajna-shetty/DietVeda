import cv2
import numpy as np

class LiveTongueScanner:
    def start_scanning(self):
        print("📸 STARTING WEBCAM... (Click on the window, then press 'Q' or ESC)")

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("❌ Could not access webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            # Box
            box = 200
            x = (w - box) // 2
            y = (h - box) // 2

            cv2.rectangle(frame, (x, y), (x + box, y + box), (0, 255, 0), 2)
            cv2.putText(frame, "PLACE TONGUE HERE", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            roi = frame[y:y+box, x:x+box]
            avg = np.mean(np.mean(roi, axis=0), axis=0)
            b, g, r = map(int, avg)

            # Diagnosis
            if r > 160 and g < 120 and b < 120:
                diag = "High Pitta (Redness)"
                color = (0, 0, 255)
            elif r > 180 and g > 180 and b > 180:
                diag = "Ama (White Coating)"
                color = (200, 200, 200)
            elif r > 130 and g < 140:
                diag = "Healthy Pink"
                color = (0, 255, 0)
            else:
                diag = "Adjust Lighting"
                color = (255, 255, 255)

            cv2.putText(frame, f"Diagnosis: {diag}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            cv2.putText(frame, f"R:{r} G:{g} B:{b}", (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow("DietVeda Live Scanner", frame)

            # 🔥 BULLETPROOF KEY DETECTION
            key = cv2.waitKey(10)

            # Covers ALL failure cases
            if key in [ord('q'), ord('Q'), 27, 113, 81]:  
                break

        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(50)
        print("📴 Scanner closed.")
