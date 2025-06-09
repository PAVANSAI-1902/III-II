# 📚 Pydantic AI: Deep Dive into Data Validation and AI Integration

## 🚀 What is Pydantic AI?
Pydantic AI is an advanced extension of the Pydantic library, designed to seamlessly integrate AI models with Python applications while ensuring strict data validation. Pydantic, known for its power in defining and validating data structures, is widely used in machine learning, AI, and API development.

## 🔍 Why Use Pydantic AI?
- ✅ **Automatic Data Validation:** Ensures data integrity before processing.
- 🔥 **Seamless AI Integration:** Makes working with AI-generated data more robust.
- 🛠 **Error Handling:** Catches incorrect or unexpected data early.
- ⚡ **Performance Efficient:** Uses optimized data parsing.
- 🔄 **Interoperability:** Works well with FastAPI, Django, and other frameworks.

---

## 📌 Where to Use Pydantic AI?
Pydantic AI is useful in multiple domains:
- **ML & AI Applications:** Validating inputs and outputs from AI models.
- **Web APIs:** Ensuring correct data formats in FastAPI, Flask, and Django.
- **Data Pipelines:** Parsing and structuring incoming datasets.
- **Chatbots & NLP Models:** Structuring responses and ensuring correctness.

---

## 🛠 Explination about EmojAI

### 1️⃣ Imported required modules
```python
import os
import requests
from pydantic import BaseModel, field_validator
from typing import List
from dotenv import load_dotenv
import random
```

### 2️⃣ Implement AI-Powered Emoji Suggestion System

#### 🎠 Define Pydantic Model
```python
from pydantic import BaseModel, field_validator
from typing import List

class EmojiSuggestion(BaseModel):
    emojis: List[str]
    message: str

    @field_validator('emojis')
    @classmethod
    def validate_emojis(cls, v):
        if len(v) < 3:
            raise ValueError("At least 3 emojis required")
        return v[:20]
```

## 🏡 Breakdown of AI-Integrated Code

### 1️⃣ Load Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()
```
🔹 `.env` file is used to store API keys securely.

🔹 `load_dotenv()` loads environment variables.

### 2️⃣ Gemini API Client for AI Integration
```python
import requests

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
```
🔹 `requests`: Used to make HTTP calls.

🔹 `os.getenv("GEMINI_API_KEY")`: Retrieves API key securely.

🔹 `raise ValueError`: Ensures API key is mandatory.

---

#### 3️⃣ Enhanced Sentiment Detection
```python
class SentimentAnalyzer:
    def __init__(self):
        self.emoji_library = {
            'happy': ["😀", "😃", "😄", "😁", "😆", "🥹", "😅", "😂", "🤣", "🥲"],
            'sad': ["😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "🥺", "😥"],
            'neutral': ["😐", "😑", "😶", "🪥", "😶‍🌫", "🙄", "😏", "😒", "🤨", "🤓"]
        }

        self.sentiment_map = {
            'happy': ["happy", "joy", "good", "great", "awesome"],
            'sad': ["sad", "bad", "upset", "unhappy"],
        }

    def detect_sentiment(self, message: str) -> str:
        lower_msg = message.lower()
        for sentiment, keywords in self.sentiment_map.items():
            if any(keyword in lower_msg for keyword in keywords):
                return sentiment
        return 'neutral'

    def get_emojis(self, sentiment: str) -> List[str]:
        return self.emoji_library.get(sentiment, self.emoji_library['neutral'])
```
🔹 **Handles API calls safely with error handling.**

🔹 **Ensures valid AI-generated responses are returned.**

---

#### 4️⃣ Gemini API Client (using gemini-2.0-flash)

```python
# --------------------------
# Gemini API Client (using gemini-2.0-flash)
# --------------------------
class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={'Content-Type': 'application/json'},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise ValueError(f"API request failed: {str(e)}")
```

### Explanation:

The `GeminiClient` class is responsible for interacting with the Gemini API (Google's generative AI model). It:

- 🔑 Retrieves the API key from environment variables.
- 📡 Defines the `generate` method, which sends a request to Gemini's endpoint with a given text prompt.
  
- 🔄 Parses the response to extract the generated text.
  
- ⚠️ Implements error handling to raise meaningful exceptions if the API request fails.

### ❓Why use the Gemini API?

✨ The Gemini API is used to generate contextually relevant text responses, such as suggesting appropriate emojis based on the sentiment of a given message. It enhances the functionality by providing more dynamic and nuanced emoji suggestions beyond a simple rule-based approach. 🎭

---


🔹 **Uses AI-generated responses** to suggest emojis based on detected sentiment.

🔹 **Includes a fallback mechanism** to return predefined emojis if the AI fails.

---

#### 5️⃣ AI Agent

```python

# --------------------------
# AI Agent
# --------------------------
class AIAgent:
    def __init__(self):
        self.gemini = GeminiClient()
        self.sentiment = SentimentAnalyzer()
    
    def suggest_emojis(self, message: str) -> EmojiSuggestion:
        try:
            sentiment = self.sentiment.detect_sentiment(message)
            prompt = f"Suggest 10 emojis for this {sentiment} message: '{message}'. Return only emojis separated by spaces."
            response = self.gemini.generate(prompt)
            emojis = response.strip().split()
            return EmojiSuggestion(emojis=emojis[:15], message=message)
        except Exception as e:
            print(f"Using fallback emojis due to: {str(e)}")
            sentiment = self.sentiment.detect_sentiment(message)
            return EmojiSuggestion(
                emojis=self.sentiment.get_emojis(sentiment),
                message=message
            )

```

## 📝 Explanation of AI Agent Code

The `AIAgent` class is responsible for analyzing the sentiment of a given message and suggesting appropriate emojis based on that sentiment. It consists of the following components:

### 🔹 **Constructor (`__init__` method)**
- Initializes two essential components:
  
  - `GeminiClient()`: An AI-based text generation model used to generate emoji suggestions.
  
  - `SentimentAnalyzer()`: A module to detect the sentiment of the input message.

### 🔹 **Emoji Suggestion (`suggest_emojis` method)**

- Takes a message as input and performs the following steps:
  
  1. **Detects Sentiment**: Uses `SentimentAnalyzer` to determine the sentiment (positive, negative, or neutral).
   
  2. **Generates Emojis**: Creates a prompt asking `GeminiClient` to suggest 10 emojis that match the detected sentiment.

  3. **Handles Errors**: If any error occurs, it falls back to a predefined set of emojis based on the sentiment.

  4. **Returns an Emoji Suggestion Object**: The function returns a structured response containing up to 15 suggested emojis along with the original message.

---

## 🤖 Different Works of This AI Agent

### ✨ **1. Sentiment Analysis** 🧐
- The AI detects whether the message expresses a positive, negative, or neutral emotion.

### 🎭 **2. Emoji Suggestion** 😍😂😢😡
- Based on the sentiment, the AI suggests a set of relevant emojis to match the tone of the message.

### 🛠 **3. Fallback Mechanism** 🚨
- If the primary AI model (`GeminiClient`) fails to generate emojis, the fallback mechanism provides predefined emoji suggestions based on sentiment.

### 📩 **4. Message Enhancement** ✍️
- By adding suitable emojis, the AI helps make messages more expressive and engaging.

### ⚡ **5. Fast and Efficient Processing** 🏎️💨
- The system ensures quick sentiment analysis and emoji generation, improving user interaction experience.

This AI Agent enhances communication by making text-based messages more engaging and expressive through accurate emoji suggestions! 🚀


# 🚀 Installation Guide of EmojAI

### Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8+
- pip (Python package manager)
- Virtual environment (optional but recommended)

### 📥 Step 1: Clone the Repository

```sh
git clone https://github.com/Pavansai20054/EmojAI
cd emojai
```

### 📦 Step 2: Create a Virtual Environment (Optional but Recommended)

```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 📌 Step 3: Install Dependencies

```sh
pip install -r requirements.txt
```

### 🔑 Step 4: Set Up Environment Variables
Create a `.env` file in the project root and add your **Gemini API Key**:

```sh
GEMINI_API_KEY=your_api_key_here
```

### ▶️ Step 5: Run the Application

```sh
python main.py
```

### ✅ You're All Set!
Now, enter a message in the CLI, and EmojAI will suggest emojis based on sentiment. 🎉🚀

---

### 🛠 Troubleshooting
- If you face issues with dependencies, try:
  
  ```sh
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
- Ensure your `.env` file is correctly configured.
- Check if the `requests` module is installed:  
  
  ```sh
  pip install requests
  ```

For any issues, feel free to open an issue in the repository! 😊

---

## 👥 Team Member
📧 **Wagmare Sanjana**: wagmaresanjana5@gmail.com  
🔗 **LinkedIn**: [Wagmare Sanjana](https://www.linkedin.com/in/wagmare-sanjana)  
🔗 **GitHub**: [Sanjana's GitHub](https://github.com/WAGMARESANJANA)  

## 📩 Contact

For any inquiries, reach out to us at: 

📧 Email: psai49779@gmail.com   
🔗 LinkedIn: https://www.linkedin.com/in/rangdal-pavansai/
