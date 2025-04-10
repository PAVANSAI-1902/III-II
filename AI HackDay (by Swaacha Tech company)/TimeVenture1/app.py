import os
from flask import Flask, request, render_template, send_file, jsonify
from flask_caching import Cache
import google.generativeai as genai
import requests
import random
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from gtts import gTTS
from io import BytesIO
from langdetect import detect
from deep_translator import GoogleTranslator
import folium
import json
import uuid
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

# Initialize API keys with fallback values for demo purposes if not provided
if not GEMINI_API_KEY:
    print("⚠️ Warning: Gemini API key missing. Using demo mode.")
    GEMINI_API_KEY = "demo_key"
if not HF_API_KEY:
    print("⚠️ Warning: HuggingFace API key missing. Using demo mode.")
    HF_API_KEY = "demo_key"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash-latest"

# Hugging Face client
hf_client = InferenceClient(token=HF_API_KEY)

# Create necessary directories
os.makedirs("static", exist_ok=True)
os.makedirs("static/audio", exist_ok=True)
os.makedirs("static/images", exist_ok=True)

# Coordinates for demo
coordinates = {
    "Golconda Fort": (17.3833, 78.4011),
    "Charminar": (17.3616, 78.4747),
    "Qutb Shahi Tombs": (17.3949, 78.3949),
    "Ramoji Film City": (17.2543, 78.6808),
    "Gateway of India": (18.9218, 72.8347),
    "Ajanta Caves": (20.5522, 75.7033),
    "Ellora Caves": (20.0268, 75.1790),
    "Shaniwar Wada": (18.5196, 73.8553),
    "Statue of Liberty": (40.6892, -74.0445),
    "Central Park": (40.7851, -73.9683),
    "Empire State Building": (40.7484, -73.9857),
    "Brooklyn Bridge": (40.7061, -73.9969),
    "Eiffel Tower": (48.8584, 2.2945),
    "Colosseum": (41.8902, 12.4922),
    "Great Wall of China": (40.4319, 116.5704),
    "Taj Mahal": (27.1751, 78.0421)
}

# Fallback data when API is not available
DEMO_PLACE_DETAILS = {
    "Golconda Fort": """
Golconda Fort is a majestic fortification located in Hyderabad, Telangana. Built in the 13th century by the Kakatiya dynasty, it later became the capital of the Qutb Shahi kingdom. The fort is known for its acoustic effects, where a clap at the entrance can be heard at the hilltop pavilion. Its ingenious water supply system and diamond mines made it one of the wealthiest forts in India during its peak.

Five interesting historical facts:
1. Golconda was once home to the famous Koh-i-Noor and Hope diamonds
2. The fort has a sophisticated water system that brought water to the highest points
3. Its acoustic design served as an early warning system against attacks
4. The fort changed hands multiple times between various dynasties
5. It eventually fell to Aurangzeb's forces after an 8-month siege in 1687

Traffic info: 
Best visited early mornings (8-10 AM) or late afternoons (3-5 PM) to avoid the heat and crowds. Weekends tend to be more crowded. Light and sound shows are held in the evenings.

Location details:
Located about 11 km west of Hyderabad's old city, Golconda Fort sits atop a granite hill. The fort complex covers approximately 11 km in circumference and has multiple defensive perimeters.
    """,
    "Charminar": """
Charminar, the iconic symbol of Hyderabad, was built in 1591 by Muhammad Quli Qutb Shah, the fifth ruler of the Qutb Shahi dynasty. The magnificent structure was constructed to commemorate the eradication of a deadly plague epidemic from the city. Its name comes from its architecture - four ('char') minarets ('minar'). The monument stands at the intersection of the old city's main thoroughfares, serving as both a mosque and a grand entrance to the city.

Five interesting historical facts:
1. It was built as a symbol of thanksgiving after a plague epidemic ended
2. The structure houses Hyderabad's oldest mosque on its top floor
3. Each side of Charminar faces a historical street known for specific trades
4. Legend says there's a secret underground tunnel connecting it to Golconda Fort
5. The four 56-meter-high minarets are said to represent the first four caliphs of Islam

Traffic info:
High congestion between 11 AM-7 PM daily. Best visited early morning (6-8 AM) for photography and peaceful exploration. The surrounding Laad Bazaar is extremely busy on weekends and holidays.

Location details:
Located in the heart of Hyderabad's old city, Charminar is surrounded by bustling markets including the famous Laad Bazaar known for its bangles and the Mecca Masjid nearby.
    """,
    "Taj Mahal": """
The Taj Mahal, located in Agra, India, is a magnificent white marble mausoleum built between 1632 and 1648 by Emperor Shah Jahan in memory of his beloved wife Mumtaz Mahal. This UNESCO World Heritage Site is considered the finest example of Mughal architecture, combining elements from Persian, Islamic, and Indian architectural styles. The main mausoleum is flanked by a mosque and a guest house, all set within a formal garden.

Five interesting historical facts:
1. Over 20,000 artisans worked on the construction of the Taj Mahal
2. The minarets are built slightly tilting outward to protect the main structure in case they collapse
3. The marble changes color subtly with the changing light of day
4. Shah Jahan was imprisoned by his son Aurangzeb in Agra Fort, with only a distant view of the Taj Mahal
5. Different types of precious and semi-precious stones were used for inlay work

Traffic info:
Peak hours are 9 AM-12 PM and 3-5 PM. Best visited at sunrise or late afternoon for fewer crowds and optimal lighting. Closed on Fridays for prayers.

Location details:
Situated on the southern bank of the Yamuna River in Agra, Uttar Pradesh. The complex spans nearly 17 hectares and includes beautiful gardens designed in the Persian charbagh style.
    """
}

@cache.memoize(timeout=3600)
def fetch_place_details(place_name, state, country):
    # If in demo mode or API fails, return demo content
    if GEMINI_API_KEY == "demo_key" or place_name in DEMO_PLACE_DETAILS:
        time.sleep(1)  # Simulate API call
        return DEMO_PLACE_DETAILS.get(place_name, "No details available in demo mode.")
    
    prompt = f"""
    Provide details about {place_name} in {state}, {country}:
    - A short historical narrative (100 words).
    - Five interesting historical facts.
    - Traffic info (peak hours, best visit times).
    - Location details.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text if response.text else "No details available."
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return f"Service temporarily unavailable. Please try again later."

@cache.memoize(timeout=3600)
def fetch_wikimedia_image(query):
    # Demo mode fallback images
    demo_images = {
        "Golconda Fort": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Golconda_Fort_Panorama.jpg/1280px-Golconda_Fort_Panorama.jpg",
        "Charminar": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Charminar-Pride_of_Hyderabad.jpg/800px-Charminar-Pride_of_Hyderabad.jpg",
        "Taj Mahal": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Taj_Mahal%2C_Agra%2C_India_edit3.jpg/1024px-Taj_Mahal%2C_Agra%2C_India_edit3.jpg"
    }
    
    if HF_API_KEY == "demo_key" or query in demo_images:
        return demo_images.get(query, None)
    
    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "opensearch",
        "search": query,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    try:
        search_resp = requests.get(search_url, params=search_params).json()
        if not search_resp[1]:
            return None
        title = search_resp[1][0]
        image_params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "piprop": "original",
            "titles": title
        }
        image_resp = requests.get(search_url, params=image_params).json()
        pages = image_resp.get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]
        return None
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

@cache.memoize(timeout=3600)
def generate_tts_audio(text, lang='en'):
    try:
        tts = gTTS(text=text[:500], lang=lang)  # Limit text length for demo
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        print(f"Error generating audio: {e}")
        # Return a simple beep sound as fallback
        return BytesIO(b'')

def analyze_sentiment(text):
    try:
        if HF_API_KEY == "demo_key":
            # Simple sentiment analysis for demo
            positive_words = ["happy", "love", "peace", "joy", "relaxing", "beautiful", "amazing"]
            negative_words = ["sad", "angry", "upset", "tired", "stressed", "terrible", "awful"]
            
            text_lower = text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                return "POSITIVE"
            elif neg_count > pos_count:
                return "NEGATIVE"
            else:
                return "NEUTRAL"
        
        output = hf_client.text_classification(text, model="cardiffnlp/twitter-roberta-base-sentiment")
        return output[0]['label']
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "NEUTRAL"

def translate_text(text, target_lang='hi'):
    try:
        if len(text) > 1000:
            text = text[:1000] + "..."  # Limit text length for demo
            
        detected_lang = detect(text)
        if detected_lang != target_lang:
            return GoogleTranslator(source='auto', target=target_lang).translate(text)
        return text
    except Exception as e:
        print(f"Error in translation: {e}")
        return "Translation service unavailable. Please try again later."

def summarize_text(text):
    try:
        if HF_API_KEY == "demo_key":
            # Simple summarization for demo - return first two sentences
            sentences = text.split('.')
            if len(sentences) > 2:
                return sentences[0] + '.' + sentences[1] + '.'
            return text
            
        summary = hf_client.summarization(
            text=text,
            model="facebook/bart-large-cnn"
        )
        return summary[0]["summary_text"]
    except Exception as e:
        print(f"Error summarizing: {e}")
        return "Summary unavailable."

def caption_image(image_url):
    try:
        if HF_API_KEY == "demo_key":
            return "A historical monument showcasing ancient architecture and cultural heritage."
            
        image = requests.get(image_url).content
        return hf_client.image_to_text(image=image, model="nlpconnect/vit-gpt2-image-captioning")
    except Exception as e:
        print(f"Error captioning image: {e}")
        return "No caption available."

def answer_question(context, question):
    try:
        if HF_API_KEY == "demo_key":
            if "built" in question.lower():
                return "It was built during the medieval period by local rulers."
            elif "visit" in question.lower():
                return "The best time to visit is during the morning hours when it's less crowded."
            else:
                return "This information isn't available in demo mode."
                
        result = hf_client.question_answering(model="deepset/roberta-base-squad2", question=question, context=context)
        return result['answer']
    except Exception as e:
        print(f"Error answering question: {e}")
        return "Sorry, I couldn't find an answer."

def get_place_recommendation(emotion, places):
    """Recommend a place based on emotion"""
    if not places:
        return None
    
    # Demo logic to match emotions to places
    emotion = emotion.lower()
    
    peaceful_places = ["Ajanta Caves", "Central Park", "Ellora Caves"]
    exciting_places = ["Ramoji Film City", "Brooklyn Bridge", "Empire State Building"]
    cultural_places = ["Charminar", "Gateway of India", "Golconda Fort"]
    
    if any(word in emotion for word in ["peace", "calm", "quiet", "relax"]):
        matches = [p for p in places if p in peaceful_places]
    elif any(word in emotion for word in ["excite", "thrill", "adventure", "fun"]):
        matches = [p for p in places if p in exciting_places]
    elif any(word in emotion for word in ["culture", "history", "learn", "education"]):
        matches = [p for p in places if p in cultural_places]
    else:
        matches = []
    
    if matches:
        return random.choice(matches)
    else:
        return random.choice(places)  # Fallback to random

def generate_itinerary(places, days=2):
    """Generate a simple itinerary based on selected places"""
    if not places or days < 1:
        return "No places selected for itinerary."
    
    itinerary = []
    places_per_day = max(1, len(places) // days)
    
    for day in range(1, days + 1):
        day_places = places[(day-1)*places_per_day:day*places_per_day]
        if not day_places:
            continue
            
        day_plan = f"Day {day}:\n"
        for i, place in enumerate(day_places):
            if i == 0:
                day_plan += f"- Morning: Visit {place} (2-3 hours)\n"
            elif i == 1:
                day_plan += f"- Afternoon: Explore {place} (2-3 hours)\n"
            else:
                day_plan += f"- Evening: Experience {place} (2 hours)\n"
        
        itinerary.append(day_plan)
    
    return "\n\n".join(itinerary)

@app.route("/", methods=["GET", "POST"])
def index():
    country = None
    state = None
    selected_places = []
    map_html = None
    details = {}
    hindi_translation = {}
    summary = {}
    sentiment = {}
    question_answer = {}
    image_url = {}
    caption = {}
    audio_path = {}
    hindi_audio_path = {}
    emotion = None
    recommendation = None
    chatbot_response = None
    itinerary = None

    states_dict = {
        "India": [None, "Telangana", "Maharashtra", "Uttar Pradesh", "Rajasthan"],
        "USA": [None, "New York", "California", "Florida"],
        "France": [None, "Île-de-France", "Provence"],
        "Italy": [None, "Lazio", "Tuscany"]
    }

    places_dict = {
        "Telangana": ["Golconda Fort", "Charminar", "Qutb Shahi Tombs", "Ramoji Film City"],
        "Maharashtra": ["Gateway of India", "Ajanta Caves", "Ellora Caves", "Shaniwar Wada"],
        "Uttar Pradesh": ["Taj Mahal", "Fatehpur Sikri", "Agra Fort"],
        "New York": ["Statue of Liberty", "Central Park", "Empire State Building", "Brooklyn Bridge"],
        "California": ["Golden Gate Bridge", "Alcatraz Island", "Hollywood Sign"],
        "Île-de-France": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"],
        "Lazio": ["Colosseum", "Roman Forum", "Vatican City"]
    }

    if request.method == "POST":
        country = request.form.get("country")
        state = request.form.get("state")
        
        # Handle AJAX request for state options
        if request.form.get("action") == "get_states":
            if country in states_dict:
                return jsonify({"states": [s for s in states_dict[country] if s]})
            return jsonify({"states": []})
            
        # Handle AJAX request for place options
        if request.form.get("action") == "get_places":
            if state in places_dict:
                return jsonify({"places": places_dict[state]})
            return jsonify({"places": []})

        if request.form.get("explore") and state:
            selected_places_list = request.form.getlist("selected_places")
            if selected_places_list:
                selected_places = selected_places_list
            else:
                available_places = places_dict.get(state, [])
                if available_places:
                    selected_places = random.sample(available_places, min(3, len(available_places)))

            if selected_places:
                # Create map
                map_center_lat = sum(coordinates.get(place, (0, 0))[0] for place in selected_places) / len(selected_places)
                map_center_lon = sum(coordinates.get(place, (0, 0))[1] for place in selected_places) / len(selected_places)
                
                m = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=5)

                for place in selected_places:
                    # Get place details and process
                    details[place] = fetch_place_details(place, state, country)
                    hindi_translation[place] = translate_text(details[place], target_lang='hi')
                    summary[place] = summarize_text(details[place])
                    
                    # Generate sentiment from sample review
                    sample_review = f"I visited {place} and it was a wonderful experience!"
                    sentiment[place] = analyze_sentiment(sample_review)
                    
                    # Process any question
                    question = request.form.get(f"question_{place}")
                    if question:
                        question_answer[place] = answer_question(details[place], question)
                    else:
                        question_answer[place] = None
                        
                    # Get image and caption
                    img_url = fetch_wikimedia_image(place)
                    image_url[place] = img_url
                    caption[place] = caption_image(img_url) if img_url else "No caption available."
                    
                    # Generate audio files
                    audio_file_id = str(uuid.uuid4())[:8]
                    
                    audio_data = generate_tts_audio(details[place][:500])  # Limit for demo
                    audio_filename = f"audio_{place}_{audio_file_id}.mp3"
                    audio_path[place] = f"static/audio/{audio_filename}"
                    
                    with open(f"static/{audio_path[place]}", "wb") as f:
                        f.write(audio_data.read())
                    
                    hindi_audio_data = generate_tts_audio(hindi_translation[place][:500], lang='hi')  # Limit for demo
                    hindi_audio_filename = f"hindi_audio_{place}_{audio_file_id}.mp3"
                    hindi_audio_path[place] = f"static/audio/{hindi_audio_filename}"
                    
                    with open(f"static/{hindi_audio_path[place]}", "wb") as f:
                        f.write(hindi_audio_data.read())

                    # Add marker to map
                    if place in coordinates:
                        lat, lon = coordinates[place]
                        popup_content = f"""
                        <strong>{place}</strong><br>
                        <img src="{image_url[place]}" width="150px"><br>
                        {summary[place][:100]}...
                        """
                        folium.Marker(
                            location=[lat, lon], 
                            popup=folium.Popup(popup_content, max_width=200),
                            icon=folium.Icon(color="red", icon="info-sign")
                        ).add_to(m)

                # Save map to HTML file
                map_file = f"static/map_{str(uuid.uuid4())[:8]}.html"
                m.save(f"static/{map_file}")
                map_html = map_file
                
                # Generate itinerary
                itinerary = generate_itinerary(selected_places, days=2)

        # Handle emotion-based recommendation
        emotion_input = request.form.get("emotion_input")
        if emotion_input:
            emotion = analyze_sentiment(emotion_input)
            if selected_places:
                recommendation = get_place_recommendation(emotion_input, selected_places)

        # Handle chatbot request
        user_q = request.form.get("historical_qa")
        if user_q:
            try:
                if GEMINI_API_KEY == "demo_key":
                    # Fallback response for demo mode
                    responses = [
                        "Greetings, traveler! The place you seek was built by ancient rulers seeking to leave their mark upon the world.",
                        "In my time, this monument was considered one of the greatest wonders of craftsmanship and engineering.",
                        "These historic structures have witnessed countless ceremonies and events of great significance.",
                        "The ancient builders employed thousands of artisans who worked tirelessly for decades to complete this monument."
                    ]
                    chatbot_response = random.choice(responses)
                else:
                    char_prompt = f"You are a 16th-century historian. Answer like an ancient royal guide. Question: {user_q}"
                    chatbot = genai.GenerativeModel(MODEL_NAME)
                    response = chatbot.generate_content(char_prompt)
                    chatbot_response = response.text
            except Exception as e:
                print(f"Chatbot error: {e}")
                chatbot_response = "The ancient scrolls are difficult to read at this moment. Please try again later."

    return render_template(
        "index.html",
        country=country,
        state=state,
        states_dict=states_dict,
        places_dict=places_dict,
        selected_places=selected_places,
        map_html=map_html,
        details=details,
        hindi_translation=hindi_translation,
        summary=summary,
        sentiment=sentiment,
        question_answer=question_answer,
        image_url=image_url,
        caption=caption,
        audio_path=audio_path,
        hindi_audio_path=hindi_audio_path,
        emotion=emotion,
        recommendation=recommendation,
        chatbot_response=chatbot_response,
        itinerary=itinerary
    )

@app.route("/upload", methods=["POST"])
def upload_file():
    if "user_image" not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files["user_image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    
    if file:
        filename = secure_filename(f"{str(uuid.uuid4())[:8]}_{file.filename}")
        filepath = os.path.join("static/images", filename)
        file.save(filepath)
        
        # Generate a caption for the uploaded image
        try:
            caption = "Your uploaded image shows a location or monument." 
            if HF_API_KEY != "demo_key":
                with open(filepath, "rb") as img_file:
                    caption = hf_client.image_to_text(
                        image=img_file.read(), 
                        model="nlpconnect/vit-gpt2-image-captioning"
                    )
        except Exception as e:
            caption = "Unable to generate caption."
            
        return jsonify({
            "success": True,
            "filename": f"images/{filename}",
            "caption": caption
        })
    
    return jsonify({"error": "Error uploading file"})

@app.route("/compare_places", methods=["POST"])
def compare_places():
    place1 = request.form.get("place1")
    place2 = request.form.get("place2")
    
    if not place1 or not place2:
        return jsonify({"error": "Two places must be selected for comparison"})
    
    try:
        # Generate a comparison in demo mode or with Gemini
        if GEMINI_API_KEY == "demo_key":
            comparison = f"""
            Comparison between {place1} and {place2}:
            
            Historical Significance:
            - {place1}: Major historical monument with significant cultural impact
            - {place2}: Important site showcasing regional architectural style
            
            Visitor Experience:
            - {place1}: Larger site with more to explore, requires 3-4 hours
            - {place2}: More compact but detailed site, can be visited in 2 hours
            
            Best For:
            - {place1}: History enthusiasts and architecture lovers
            - {place2}: Photography and cultural immersion
            """
        else:
            prompt = f"Compare {place1} and {place2} in terms of historical significance, visitor experience, and what type of traveler would enjoy each more. Format as bullet points."
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)
            comparison = response.text
            
        return jsonify({"success": True, "comparison": comparison})
    except Exception as e:
        return jsonify({"error": f"Error generating comparison: {str(e)}"})

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    os.makedirs("static/audio", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)
    app.run(debug=True)