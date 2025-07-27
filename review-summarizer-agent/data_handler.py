import json
import csv
from typing import List, Dict
import os


class DataHandler:
    @staticmethod
    def load_reviews_from_json(file_path: str) -> List[Dict]:
        """Load reviews from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else [data]
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return []

    @staticmethod
    def load_reviews_from_csv(file_path: str, review_column: str = "review") -> List[str]:
        """Load reviews from CSV file"""
        reviews = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if review_column in row and row[review_column].strip():
                        reviews.append(row[review_column].strip())
        except Exception as e:
            print(f"Error loading CSV: {e}")
        return reviews

    @staticmethod
    def save_summary(summary_data: Dict, output_path: str):
        """Save summary to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            print(f"Summary saved to {output_path}")
        except Exception as e:
            print(f"Error saving summary: {e}")

    @staticmethod
    def create_sample_reviews(file_path: str):
        """Create sample reviews for testing"""
        sample_reviews = [
            "Amazing food and great service! The pasta was perfectly cooked and the staff was very friendly. Highly recommend!",
            "Good location but the food was cold when it arrived. Service was slow and the prices are too high for the quality.",
            "Beautiful ambiance and excellent customer service. The desserts were incredible. Will definitely come back!",
            "Disappointing experience. Long wait times and the food was mediocre at best. Not worth the money.",
            "Clean restaurant with decent food. Nothing spectacular but good value for money. Staff was helpful.",
            "Outstanding experience! Every dish was perfect and the atmosphere was romantic. Perfect for date night.",
            "Terrible service and rude staff. Food was okay but the experience was ruined by poor service.",
            "Great place for families! Kids loved it and adults enjoyed the food too. Reasonable prices.",
            "Food was fresh and delicious. Quick service and clean environment. Will order again!",
            "Not impressed. Food was bland and overpriced. Better options available in the area."
        ]

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "place_name": "Sample Restaurant",
                    "reviews": sample_reviews
                }, f, indent=2)
            print(f"Sample reviews created at {file_path}")
        except Exception as e:
            print(f"Error creating sample file: {e}")