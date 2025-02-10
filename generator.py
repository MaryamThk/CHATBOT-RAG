import json 
import requests

class Generator:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url

    def generate(self, prompt, max_length=100):
        """
        Generate a response using the Ollama local server.
        - `prompt`: The input text (e.g., "What is Python?").
        - `max_length`: Maximum length of the generated response.
        """
        data = {
            "model": "deepseek-r1",  # The model name you're using with Ollama
            "prompt": prompt,
            "max_tokens": max_length,
            "temperature": 0.7  # Adjust for creativity vs. determinism
        }
        try:
            # Send the request to Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=data,
                stream=True  # Enable streaming
            )
            response.raise_for_status()  # Raise an error for bad status codes

            # Process the streaming response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    # Decode the line and parse it as JSON
                    chunk = json.loads(line.decode("utf-8"))
                    # Append the response chunk to the full response
                    full_response += chunk.get("response", "")

                    # Stop if the response is done
                    if chunk.get("done", False):
                        break

            # Return the full response
            return full_response.strip()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            return "Sorry, I couldn't generate a response."