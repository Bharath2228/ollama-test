from ollama_client import OllamaClient
from typing import List, Dict
import re


class ReviewSummarizer:
    def __init__(self):
        self.client = OllamaClient()

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text

    def create_summary_prompt(self, reviews: List[str], place_name: str = "") -> str:
        """Create a structured prompt for summarization"""
        reviews_text = ""
        for i, review in enumerate(reviews, 1):
            clean_review = self.clean_text(review)
            reviews_text += f"Review {i}: {clean_review}\n\n"

        prompt = f"""
You are a helpful assistant that summarizes customer reviews for places/businesses.

Place: {place_name if place_name else "Unknown"}

Reviews to summarize:
{reviews_text}

Please provide a comprehensive summary that includes:
1. Overall sentiment (Positive/Negative/Mixed)
2. Most commonly mentioned positive aspects
3. Most commonly mentioned negative aspects  
4. Key themes and patterns
5. Brief recommendation

Keep the summary concise but informative (150-300 words).

Summary:"""

        return prompt

    def summarize_reviews(self, reviews: List[str], place_name: str = "") -> Dict:
        """Summarize a list of reviews"""
        if not reviews:
            return {"error": "No reviews provided"}

        if not self.client.is_available():
            return {"error": "Ollama service is not available. Please ensure Ollama is running."}

        # Limit reviews to prevent token overflow
        max_reviews = 10
        if len(reviews) > max_reviews:
            reviews = reviews[:max_reviews]

        prompt = self.create_summary_prompt(reviews, place_name)

        try:
            summary = self.client.generate_response(prompt, max_tokens=400)

            # Parse sentiment from summary (simple approach)
            sentiment = "Mixed"
            if "positive" in summary.lower() and "negative" not in summary.lower():
                sentiment = "Positive"
            elif "negative" in summary.lower() and "positive" not in summary.lower():
                sentiment = "Negative"

            return {
                "summary": summary,
                "sentiment": sentiment,
                "total_reviews": len(reviews),
                "place_name": place_name
            }

        except Exception as e:
            return {"error": f"Error generating summary: {str(e)}"}

    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of a single review"""
        prompt = f"""
Analyze the sentiment of this review and respond with only one word: Positive, Negative, or Neutral.

Review: {self.clean_text(text)}

Sentiment:"""

        try:
            result = self.client.generate_response(prompt, max_tokens=10)
            sentiment = result.strip().title()
            if sentiment in ["Positive", "Negative", "Neutral"]:
                return sentiment
            return "Neutral"
        except:
            return "Neutral"