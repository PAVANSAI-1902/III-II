import os
import streamlit as st
import google.generativeai as genai
import requests
import random
import time  

# 🔑 Load API Keys
try:
    import api_keys
    GEMINI_API_KEY = api_keys.gemini_api
except ImportError:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ API key missing. Set it as an environment variable or provide api_keys.py locally.")

# ✅ Configure Free Gemini API
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash"

# ✅ Function to Fetch Place Details
def fetch_place_details(place_name, state, country):
    prompt = f"""
    Provide details about {place_name} in {state}, {country}:
    - 🌍 A short historical narrative (100 words).
    - 📜 Five interesting historical facts.
    - 🚦 Traffic info (peak hours, best visit times).
    - 📍 Location details.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text if response.text else "No details available."
    except Exception as e:
        return f"⚠️ Error retrieving details: {e}"

# ✅ Function to Fetch Wikimedia Images
@st.cache_data
def fetch_wikimedia_image(query):
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "piprop": "original",
        "titles": query
    }
    try:
        response = requests.get(url, params=params).json()
        pages = response.get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]
    except Exception:
        return None

# ✅ Streamlit App
def main():
    st.title("🏛️ Historical Places Explorer")
    st.write("🔍 Discover famous historical places!")

    country = st.selectbox("🌍 Select Country", [None, "India", "USA"])
    
    states_dict = {
        "India": [None, "Telangana", "Maharashtra"],
        "USA": [None, "New York"]
    }
    
    if country:
        state = st.selectbox("📍 Select State", states_dict[country])
    else:
        state = None

    if state and st.button("🗺️ Get Details"):
        st.subheader(f"🏰 Historical Places in {state}, {country}")
        
        places = {
            "Telangana": ["Golconda Fort", "Charminar", "Qutb Shahi Tombs", "Ramoji Film City", "Bhongir Fort", "Warangal Fort", "Thousand Pillar Temple", "Chowmahalla Palace", "Paigah Tombs", "Mecca Masjid", "Taramati Baradari", "Birla Mandir", "Medak Fort", "Kakatiya Kala Thoranam", "Salar Jung Museum", "Purani Haveli", "Falaknuma Palace", "Basar Saraswati Temple", "Khammam Fort", "Jadcherla Fort", "Elgandal Fort", "Kondapalli Fort", "Ananda Buddha Vihara", "Sri Raja Rajeshwara Temple", "Ghanpur Temples"],
            "Maharashtra": ["Gateway of India", "Ajanta Caves", "Ellora Caves", "Shaniwar Wada", "Raigad Fort", "Sinhagad Fort", "Daulatabad Fort", "Chhatrapati Shivaji Terminus", "Kanheri Caves", "Elephanta Caves", "Lohagad Fort", "Rajmachi Fort", "Pratapgad Fort", "Janjira Fort", "Pandavleni Caves", "Karla Caves", "Bhimashankar Temple", "Trimbakeshwar Temple", "Vikramshila University", "Bassein Fort", "Aurangabad Caves", "Harihar Fort", "Panhala Fort", "Tung Fort", "Sudhagad Fort"],
            "New York": ["Statue of Liberty", "Brooklyn Bridge", "Empire State Building", "Central Park", "Times Square", "One World Trade Center", "Rockefeller Center", "Metropolitan Museum of Art", "Grand Central Terminal", "Ellis Island", "St. Patrick's Cathedral", "Carnegie Hall", "Flatiron Building", "Radio City Music Hall", "Wall Street", "Chrysler Building", "New York Public Library", "Broadway Theatre District", "American Museum of Natural History", "Federal Hall", "Solomon R. Guggenheim Museum", "Bryant Park", "Madison Square Garden", "Cathedral of St. John the Divine", "The High Line"]
        }
        
        selected_places = random.sample(places.get(state, []), 6)
        
        for place in selected_places:
            st.subheader(f"🏰 {place}")
            
            image_url = fetch_wikimedia_image(place)
            
            if image_url:
                st.image(image_url, caption=place, use_container_width=True)
            else:
                st.write("❌ No image found.")
            
            time.sleep(1)
            details = fetch_place_details(place, state, country)
            st.write(details)

if __name__ == "__main__":
    main()