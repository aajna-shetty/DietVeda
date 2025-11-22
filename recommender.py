import pandas as pd
import datetime

class DietRecommender:
    def __init__(self, dishes_file):
        # Load Data
        self.df = pd.read_csv(dishes_file)
        # Fill NaNs to prevent errors
        self.df['avoids_for'] = self.df['avoids_for'].fillna('')
        self.df['season'] = self.df['season'].fillna('All')

    def _get_season(self):
        """
        Engineering Touch: Automatically detect the season based on current month.
        """
        month = datetime.datetime.now().month
        if month in [11, 12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5, 6]:
            return 'Summer'
        else:
            return 'Monsoon'  # Simplified for Indian context

    def _calculate_score(self, row, primary_dosha, secondary_dosha, current_season):
        """
        The Core Algorithm: Assigns a 'Suitability Score' to every dish.
        """
        score = 0
        
        suitable_list = row['dosha_suitable_for']
        avoids_list = row['avoids_for']
        
        # 1. Safety Check (CRITICAL)
        # If it aggravates either dosha, kill the score (set to -100)
        if primary_dosha in avoids_list or (secondary_dosha and secondary_dosha in avoids_list):
            return -100

        # 2. Dosha Matching
        if primary_dosha in suitable_list:
            score += 10  # High priority
            
        if secondary_dosha and secondary_dosha in suitable_list:
            score += 5   # Medium priority for secondary dosha
            
        # 3. Tridoshic Bonus (Good for everyone)
        if "Kapha, Pitta, Vata" in suitable_list:
            score += 3

        # 4. Seasonal Adjustment
        # If dish is for 'All' seasons or matches current season
        if row['season'] == 'All' or current_season in row['season']:
            score += 5
        elif row['season'] != 'All' and current_season not in row['season']:
            score -= 5  # Penalty for wrong season (e.g., Ice cream in Winter)

        return score

    def recommend(self, user_dosha, meal_type=None):
        """
        Main function to get ranked recommendations.
        user_dosha can be "Vata", "Pitta", or "Vata-Pitta"
        """
        # Handle Dual Doshas (e.g., "Vata-Pitta")
        if "-" in user_dosha:
            parts = user_dosha.split("-")
            primary = parts[0]
            secondary = parts[1]
        else:
            primary = user_dosha
            secondary = None

        current_season = self._get_season()
        
        # Apply the Scoring Algorithm to every row
        # We use a lambda function to apply logic row-by-row
        self.df['score'] = self.df.apply(
            lambda row: self._calculate_score(row, primary, secondary, current_season), 
            axis=1
        )

        # Filter out "Dangerous" foods (Score < 0)
        safe_foods = self.df[self.df['score'] > 0].copy()

        # Filter by Meal Type if provided (e.g., "Breakfast")
        if meal_type:
            safe_foods = safe_foods[safe_foods['dish_type'].str.lower() == meal_type.lower()]

        # Sort by Score (High to Low) -> The "Best" matches first
        ranked_foods = safe_foods.sort_values(by='score', ascending=False)
        
        return ranked_foods[['dish_name', 'dish_type', 'season', 'score', 'ingredients']].head(10)

# --- SIMULATION ---
if __name__ == "__main__":
    # Initialize System
    recommender = DietRecommender("dishes_dataset.csv")
    
    # Scenario 1: A Complex User (Vata-Pitta) asking for Dinner
    user_dosha = "Vata-Pitta"
    print(f"🥗 Recommendations for {user_dosha} (Sorted by Relevance):")
    
    results = recommender.recommend(user_dosha, meal_type="Dinner")
    
    # Display nicely
    print(results.to_string(index=False))