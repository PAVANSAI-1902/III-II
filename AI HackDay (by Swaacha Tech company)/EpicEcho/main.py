import streamlit as st
import google.generativeai as genai
import api_keys  # Ensure you have your API key stored securely
import requests
import random

# 🔑 Configure Free Gemini API
GEMINI_API_KEY = api_keys.gemini_api  # Load API Key
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Use a Free-Tier Model
MODEL_NAME = "gemini-1.5-flash"  # Use "gemini-1.0-pro" if needed

@st.cache_data
def fetch_place_details(place_name, state, country):
    prompt = f"""
    Provide details about {place_name} in {state}, {country}:
    - 🌜 A short historical narrative (100 words).
    - 📚 Two interesting historical facts.
    - 🚦 Traffic info (peak hours, best visit times).
    - 📍 Location details.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text if response.text else "No details available."
    except Exception as e:
        return f"⚠️ Error retrieving details: {e}"

@st.cache_data
def fetch_wikipedia_image(place_name):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place_name.replace(' ', '_')}"
        response = requests.get(url).json()
        return response.get("thumbnail", {}).get("source", None)
    except Exception as e:
        return None

# 🌍 Run Streamlit App
def main():
    st.title("🏡 Historical Places Explorer")
    st.write("🔍 Discover famous historical places!")

    country = st.selectbox("🌐 Select Country", ["India", "USA"])
    states_dict = {
        "India": ["Telangana", "Maharashtra", "Tamil Nadu"],
        "USA": ["NYC"]
    }
    state = st.selectbox("📍 Select State", states_dict[country])
    
    if st.button("🗺️ Get Details"):
        st.subheader(f"🏢 Historical Places in {state}, {country}")
        
        places = {
            "Telangana": ["Golconda Fort", "Charminar", "Qutb Shahi Tombs", "Chowmahalla Palace", "Mecca Masjid", "Falaknuma Palace", "Kakatiya Kala Thoranam", "Bhongir Fort", "Warangal Fort", "Taramati Baradari", "Ramappa Temple", "Thousand Pillar Temple", "Purani Haveli", "Paigah Tombs", "Khammam Fort"],
            "Maharashtra": ["Gateway of India", "Ajanta Caves", "Ellora Caves", "Chhatrapati Shivaji Terminus", "Elephanta Caves", "Shaniwar Wada", "Raigad Fort", "Daulatabad Fort", "Siddhivinayak Temple", "Kanheri Caves", "Lal Mahal", "Jijamata Udyaan", "Karla Caves", "Pratapgad Fort", "Bibi Ka Maqbara"],
            "Tamil Nadu": ["Brihadeeswarar Temple", "Mahabalipuram Shore Temple", "Meenakshi Temple", "Ramanathaswamy Temple", "Fort St. George", "Kapaleeshwarar Temple", "Thanjavur Palace", "Vivekananda Rock Memorial", "Gangaikonda Cholapuram", "Arjuna's Penance", "Kumbakonam Temples", "Srirangam Temple", "Rockfort Temple", "Thirumalai Nayakkar Mahal", "Ekambareswarar Temple"],
            "NYC": ["Statue of Liberty", "Empire State Building", "Brooklyn Bridge", "Central Park", "Times Square", "Wall Street", "Ellis Island", "Grand Central Terminal", "Chrysler Building", "One World Trade Center", "Metropolitan Museum of Art", "St. Patrick's Cathedral", "Flatiron Building", "Rockefeller Center", "The High Line"]
        }

        selected_places = random.sample(places.get(state, []), 6)

        for place in selected_places:
            st.subheader(f"🏰 {place}")
            image_url = fetch_wikipedia_image(place)
            if image_url:
                st.image(image_url, caption=place, use_container_width=True)
            details = fetch_place_details(place, state, country)
            st.write(details)

if __name__ == "__main__":
    main()