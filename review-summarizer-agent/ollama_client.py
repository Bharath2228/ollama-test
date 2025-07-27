import requests
import json
from typing import List, Dict, Optional

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "gemma3:1b"

    def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.3
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except json.JSONDecodeError as e:
            return f"Error parsing response: {str(e)}"


    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False