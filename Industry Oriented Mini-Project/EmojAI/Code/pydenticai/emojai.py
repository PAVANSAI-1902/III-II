import random
import re
from pydantic import BaseModel
from typing import List, Tuple, Optional

# --------------------------
# Pydantic Models
# --------------------------
class EmojiSuggestion(BaseModel):
    emojis: List[str]
    message: str
    explanation: Optional[str] = None

# --------------------------
# Sentiment Analysis
# --------------------------
class SentimentAnalyzer:
    """Analyzes text sentiment and suggests appropriate emojis."""

    def __init__(self):
        # Emoji library with unique emojis per category and intensity
        self.emoji_library = {
            'happy': {
                'mild': ["😊", "🙂", "😄", "😀"],
                'moderate': ["😃", "😁", "😆"],
                'strong': ["🤩", "🥳", "😻", "🎉", "🎊"]
            },
            'sad': {
                'mild': ["😔", "😞", "🥺", "😟"],
                'moderate': ["😢", "😥", "😭"],
                'strong': ["😩", "😣", "😿", "💔"]
            },
            'love': {
                'mild': ["🥰", "😍", "❤️", "😘"],
                'moderate': ["💖", "💕", "💞", "💓"],
                'strong': ["💘", "💝", "💟"]
            },
            'excited': {
                'mild': ["😎", "😏", "😺", "🤩"],
                'moderate': ["🤩", "🥳", "😻", "🙌"],
                'strong': ["🚀", "🔥", "🎉", "🎊"]
            },
            'greeting': {
                'mild': ["👋", "🤚", "🖐️", "🤝"],
                'moderate': ["✌️", "🤞", "👌", "🤙"],
                'strong': ["🤟", "🖖", "✋", "🙏"]
            },
            'angry': {
                'mild': ["😠", "😒", "😤"],
                'moderate': ["😡", "🤬"],
                'strong': ["👿"]
            },
            'danger': {
                'mild': ["⚠️", "🚨", "🆘", "💀"],
                'moderate': ["😰", "😨", "😬", "😱"],
                'strong': ["🔥", "💣", "💥"]
            },
            'confused': {
                'mild': ["😕", "🤔", "🧐", "🤷"],
                'moderate': ["😖", "😣", "🤨", "😟"],
                'strong': ["😵", "😓", "🤯", "❓"]
            },
            'neutral': {
                'mild': ["😐", "😑", "😶", "😌"],
                'moderate': ["😒", "🙄", "😏", "😶"],
                'strong': ["🤨", "🧐", "🗿", "🧊"]
            },
            'mixed': {
                'happy_sad': ["😊😢", "😄😔", "🥲"],
                'excited_nervous': ["🤩😬", "😃😅", "😁😰"],
                'love_hate': ["🥰😒", "😍🙄"],
                'angry_confused': ["😡😕", "🤬🤔"]
            }
        }

        # Sentiment keywords
        self.sentiment_map = {
            'happy': ["happy", "joy", "good", "great", "awesome", "cheerful"],
            'sad': ["sad", "bad", "upset", "unhappy", "depressed"],
            'love': ["love", "heart", "adore", "cherish"],
            'excited': ["excited", "wow", "amazing", "thrilled"],
            'greeting': ["hello", "hi", "hey", "greetings"],
            'angry': ["angry", "furious", "mad", "irritated"],
            'danger': ["danger", "warning", "alert", "emergency"],
            'confused': ["confused", "why", "huh", "what"],
            'nervous': ["nervous", "anxious", "worried", "apprehensive"]
        }

        # Mixed emotion patterns
        self.mixed_patterns = [
            ({"happy", "sad"}, "happy_sad"),
            ({"excited", "nervous"}, "excited_nervous"),
            ({"love", "angry"}, "love_hate"),
            ({"angry", "confused"}, "angry_confused")
        ]

        # Strong keywords in lowercase
        self.strong_keywords = {
            "marvelous", "amazing", "wonderful", "terrible",
            "horrible", "furious", "enraged", "urgent"
        }

        self.intensity_words = {
            'slightly': 1, 'a little': 1, 'very': 2, 'really': 2,
            'extremely': 3, 'seriously': 3, 'so': 2, 'completely': 3
        }

        self.intensity_levels = {1: 'mild', 2: 'moderate', 3: 'strong'}

        # Sentiment priority with default
        self.sentiment_priority = {
            'excited': 1, 'love': 2, 'happy': 3, 'angry': 4,
            'danger': 5, 'sad': 6, 'nervous': 7, 'greeting': 8,
            'confused': 9, 'neutral': 10
        }

    def detect_sentiment(self, message: str) -> List[Tuple[str, int]]:
        """Detects sentiments and their intensities in a message."""
        lower_msg = message.lower()
        words = re.findall(r'\b\w+\b|[^\w\s]', lower_msg)
        sentiment_intensities = {}

        # Detect base sentiments
        for sent, keywords in self.sentiment_map.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', lower_msg):
                    base_intensity = 3 if keyword in self.strong_keywords else 1
                    if sent not in sentiment_intensities or base_intensity > sentiment_intensities[sent]:
                        sentiment_intensities[sent] = base_intensity

        # Adjust intensity based on modifiers
        for sent, current_intensity in list(sentiment_intensities.items()):
            for keyword in self.sentiment_map.get(sent, []):
                keyword_indices = [i for i, word in enumerate(words) if word == keyword]
                for idx in keyword_indices:
                    for i in range(max(0, idx - 3), idx):
                        if words[i] in self.intensity_words:
                            sentiment_intensities[sent] = max(
                                current_intensity,
                                self.intensity_words[words[i]]
                            )

        # Handle question marks
        if "?" in message and 'confused' not in sentiment_intensities:
            sentiment_intensities['confused'] = 1

        # Add neutral if no strong sentiment detected
        if not sentiment_intensities:
            sentiment_intensities['neutral'] = 1

        # Sort by priority
        detected_sentiments = sorted(
            sentiment_intensities.items(),
            key=lambda x: self.sentiment_priority.get(x[0], 99)
        )

        return detected_sentiments

    def get_mixed_emotion(self, sentiments: List[Tuple[str, int]]) -> Optional[str]:
        """Identifies mixed emotions based on detected sentiments."""
        sentiment_set = {s[0] for s in sentiments}
        for pattern, mixed_type in self.mixed_patterns:
            if pattern.issubset(sentiment_set):
                # Allow mixed emotions for any intensity (≥1) when both sentiments are present
                intensities = {s[0]: s[1] for s in sentiments}
                if all(intensities.get(sent, 0) >= 1 for sent in pattern):
                    return mixed_type
        return None

    def get_emojis(self, sentiments: List[Tuple[str, int]]) -> Tuple[List[str], Optional[str]]:
        """Selects emojis based on detected sentiments."""
        if not sentiments:
            return [random.choice(self.emoji_library['neutral']['mild'])], "No sentiment detected, defaulting to neutral."

        # Check for mixed emotions
        mixed_type = self.get_mixed_emotion(sentiments)
        if mixed_type:
            mixed_emojis = self.emoji_library['mixed'].get(mixed_type, [])
            if mixed_emojis:
                explanation = f"Mixed emotions detected: {mixed_type.replace('_', ' + ')}."
                return [random.choice(mixed_emojis)], explanation

        # Primary sentiment logic
        primary_sentiment, primary_intensity = sentiments[0]
        intensity_level = self.intensity_levels.get(primary_intensity, 'mild')

        # Fallback to neutral if sentiment not in emoji_library
        emoji_options = self.emoji_library.get(primary_sentiment, {}).get(
            intensity_level, self.emoji_library['neutral']['mild']
        )
        primary_emoji = random.choice(emoji_options)

        # Secondary emoji if applicable
        secondary_emoji = None
        explanation = f"Primary sentiment: {primary_sentiment} ({intensity_level})."
        if len(sentiments) > 1 and sentiments[1][1] >= 2:
            secondary_sentiment, secondary_intensity = sentiments[1]
            sec_intensity_level = self.intensity_levels.get(secondary_intensity, 'mild')
            secondary_options = self.emoji_library.get(secondary_sentiment, {}).get(
                sec_intensity_level, []
            )
            if secondary_options:
                secondary_emoji = random.choice(secondary_options)
                explanation += f" Secondary sentiment: {secondary_sentiment} ({sec_intensity_level})."
        elif len(sentiments) > 1:
            explanation += f" Secondary sentiment ({sentiments[1][0]}) not strong enough for emoji."

        emojis = [primary_emoji]
        if secondary_emoji:
            emojis.append(secondary_emoji)

        return emojis, explanation

# --------------------------
# AI Agent
# --------------------------
class AIAgent:
    """Generates emoji suggestions based on text analysis."""

    def __init__(self):
        self.sentiment = SentimentAnalyzer()

    def suggest_emojis(self, message: str) -> EmojiSuggestion:
        """Suggests emojis for a given message."""
        try:
            sentiments = self.sentiment.detect_sentiment(message)
            emojis, explanation = self.sentiment.get_emojis(sentiments)
            return EmojiSuggestion(
                emojis=emojis,
                message=message,
                explanation=explanation
            )
        except Exception as e:
            print(f"Error in emoji suggestion: {e}")
            return EmojiSuggestion(
                emojis=["❓"],
                message=message,
                explanation="Error processing message"
            )

# --------------------------
# CLI Interface
# --------------------------
def main():
    """Runs the CLI interface for emoji suggestion."""
    print("\n🌟 Advanced Emoji Suggester 🌟")
    print("----------------------------")
    print("Now with mixed emotion support!")
    print("Type 'q' to quit\n")

    agent = AIAgent()

    while True:
        try:
            message = input("Your message: ").strip()
            if message.lower() == 'q':
                print("\nGoodbye! 👋")
                break

            if not message:
                print("Please enter a message.")
                continue

            if len(message) > 1000:
                print("Message too long. Please keep it under 1000 characters.")
                continue

            suggestion = agent.suggest_emojis(message)
            print(f"\nFor: {suggestion.message}")
            print("Emojis:", " ".join(suggestion.emojis))
            if suggestion.explanation:
                print("Note:", suggestion.explanation)
            print("="*50 + "\n")

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()