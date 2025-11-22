# analytics.py
import datetime
import matplotlib.pyplot as plt
from progress_db import ProgressDB
import os
import numpy as np
import statistics

class WellnessAnalytics:
    def __init__(self):
        self.db = ProgressDB()

    def _normalize_dates_scores(self, rows):
        """
        Support MULTIPLE scores per day.
        If a day has multiple entries → average the scores.
        """
        # Build a dict: date → list of (dosha, score)
        dmap = {}
        for date, dosha, score in rows:
            dmap.setdefault(date, []).append((dosha, score))

        today = datetime.date.today()
        dates = []
        scores = []
        doshas = []

        # Build last 30 days (oldest → newest)
        for i in range(29, -1, -1):
            day = today - datetime.timedelta(days=i)
            day_s = str(day)
            dates.append(day_s)

            if day_s in dmap:
                score_list = [s for _, s in dmap[day_s]]
                avg_score = sum(score_list) / len(score_list)

                most_recent_dosha = dmap[day_s][-1][0]

                scores.append(avg_score)
                doshas.append(most_recent_dosha)
            else:
                scores.append(None)
                doshas.append(None)

        return dates, scores, doshas

    def generate_progress_graph(self, out_path="progress.png"):
        rows = self.db.get_last_30_days()
        if not rows:
            print("❌ No progress data yet. Do a routine first.")
            return None

        dates, scores, doshas = self._normalize_dates_scores(rows)

        y = [(np.nan if s is None else s) for s in scores]

        plt.figure(figsize=(10,4.5))
        plt.plot(dates, y, marker='o', linewidth=2, label="Sattva Score")
        plt.ylim(-5, 110)
        plt.title("30-Day Wellness Progress — Sattva Score")
        plt.xlabel("Date")
        plt.ylabel("Score")
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.savefig(out_path)
        plt.close()
        print(f"📈 Progress graph saved to {out_path}")
        return out_path

    def generate_insights(self):
        rows = self.db.get_last_30_days()
        if not rows:
            return "No data yet — start tracking daily to get insights."

        _, scores_raw, doshas_raw = self._normalize_dates_scores(rows)

        paired = [(d, s) for d, s in zip(doshas_raw, scores_raw) if s is not None]
        if not paired:
            return "Not enough scored days to generate insights."

        doshas = [p[0] for p in paired]
        scores = [p[1] for p in paired]

        insight_lines = []

        if len(doshas) >= 3 and all(d == "Pitta" for d in doshas[-3:]):
            insight_lines.append("🔥 Your Pitta has been high for 3 consecutive days.")

        if len(scores) >= 3 and all(s < 50 for s in scores[-3:]):
            insight_lines.append("⚠️ Sattva score low for 3 days.")

        if len(scores) >= 7:
            last7 = scores[-7:]
            if last7[-1] > last7[0]:
                insight_lines.append("📈 Positive weekly improvement!")
            elif last7[-1] < last7[0]:
                insight_lines.append("🔻 Weekly decline in performance.")

        if len(scores) >= 5:
            sd = statistics.pstdev(scores)
            if sd < 8:
                insight_lines.append("✨ Very stable routine!")
            else:
                insight_lines.append("🔄 Routine varies a lot — try for consistency.")

        if not insight_lines:
            return "✨ No strong signals. Keep tracking for richer insights."

        return "\n".join(insight_lines)


# CLI Test
if __name__ == "__main__":
    wa = WellnessAnalytics()
    wa.generate_progress_graph()
    print("--- Insights ---")
    print(wa.generate_insights())
