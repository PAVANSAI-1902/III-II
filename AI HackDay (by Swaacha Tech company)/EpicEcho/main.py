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
@st.cache_data(ttl=3600)
def fetch_wikimedia_image(query):
    # Map place names to their correct Wikipedia titles
    place_mapping = {
        # Telangana
        "Golconda Fort": "Golkonda Fort",
        "Charminar": "Charminar",
        "Qutb Shahi Tombs": "Qutb Shahi Tombs",
        "Ramoji Film City": "Ramoji Film City",
        "Bhongir Fort": "Bhongir Fort",
        "Warangal Fort": "Warangal Fort",
        "Thousand Pillar Temple": "Thousand Pillar Temple",
        "Chowmahalla Palace": "Chowmahalla Palace",
        "Paigah Tombs": "Paigah Tombs",
        "Mecca Masjid": "Mecca Masjid, Hyderabad",
        "Taramati Baradari": "Taramati Baradari",
        "Birla Mandir": "Birla Mandir, Hyderabad",
        "Medak Fort": "Medak Fort",
        "Kakatiya Kala Thoranam": "Kakatiya Kala Thoranam",
        "Salar Jung Museum": "Salar Jung Museum",
        "Purani Haveli": "Purani Haveli",
        "Falaknuma Palace": "Falaknuma Palace",
        "Basar Saraswati Temple": "Gnana Saraswati Temple, Basar",
        "Khammam Fort": "Khammam Fort",
        "Jadcherla Fort": "Jadcherla Fort",
        "Elgandal Fort": "Elgandal Fort",
        "Kondapalli Fort": "Kondapalli Fort",
        "Ananda Buddha Vihara": "Ananda Buddha Vihara",
        "Sri Raja Rajeshwara Temple": "Sri Raja Rajeshwara Temple",
        "Ghanpur Temples": "Ghanpur Temples",
        "Pochampally": "Pochampally",
        "Nizamabad Fort": "Nizamabad Fort",
        "Kolanupaka Temple": "Kolanupaka Temple",
        "Alampur Temples": "Alampur Temples",
        "Nagulapalli": "Nagulapalli",
        "Pillalamarri": "Pillalamarri",
        "Kaleshwaram Temple": "Kaleshwaram Temple",
        "Yadagirigutta Temple": "Yadagirigutta Temple",
        "Vemulawada Temple": "Vemulawada Temple",
        "Bhadrachalam Temple": "Bhadrachalam Temple",
        "Kulpakji Jain Temple": "Kulpakji Jain Temple",
        "Nalgonda Fort": "Nalgonda Fort",
        "Mahabubnagar Fort": "Mahabubnagar Fort",
        "Adilabad Fort": "Adilabad Fort",
        "Nirmal Fort": "Nirmal Fort",
        "Karimnagar Fort": "Karimnagar Fort",
        "Sanghi Temple": "Sanghi Temple",
        "Dharmapuri Temple": "Dharmapuri Temple",
        "Jagtial Fort": "Jagtial Fort",
        "Manthani Temple": "Manthani Temple",
        "Nizam Sagar": "Nizam Sagar",
        "Papi Hills": "Papi Hills",
        "Pakhal Lake": "Pakhal Lake",
        "Ramappa Temple": "Ramappa Temple",
        "Laknavaram Lake": "Laknavaram Lake",
        "Kawal Wildlife Sanctuary": "Kawal Wildlife Sanctuary",

        # Maharashtra
        "Gateway of India": "Gateway of India",
        "Ajanta Caves": "Ajanta Caves",
        "Ellora Caves": "Ellora Caves",
        "Shaniwar Wada": "Shaniwar Wada",
        "Raigad Fort": "Raigad Fort",
        "Sinhagad Fort": "Sinhagad Fort",
        "Daulatabad Fort": "Daulatabad Fort",
        "Chhatrapati Shivaji Terminus": "Chhatrapati Shivaji Terminus",
        "Kanheri Caves": "Kanheri Caves",
        "Elephanta Caves": "Elephanta Caves",
        "Lohagad Fort": "Lohagad Fort",
        "Rajmachi Fort": "Rajmachi Fort",
        "Pratapgad Fort": "Pratapgad Fort",
        "Janjira Fort": "Janjira Fort",
        "Pandavleni Caves": "Pandavleni Caves",
        "Karla Caves": "Karla Caves",
        "Bhimashankar Temple": "Bhimashankar Temple",
        "Trimbakeshwar Temple": "Trimbakeshwar Temple",
        "Vikramshila University": "Vikramshila University",
        "Bassein Fort": "Bassein Fort",
        "Aurangabad Caves": "Aurangabad Caves",
        "Harihar Fort": "Harihar Fort",
        "Panhala Fort": "Panhala Fort",
        "Tung Fort": "Tung Fort",
        "Sudhagad Fort": "Sudhagad Fort",
        "Sindhudurg Fort": "Sindhudurg Fort",
        "Murud-Janjira Fort": "Murud-Janjira Fort",
        "Kolhapur Palace": "Kolhapur Palace",
        "Mahabaleshwar Temple": "Mahabaleshwar Temple",
        "Ratnagiri Fort": "Ratnagiri Fort",
        "Vijaydurg Fort": "Vijaydurg Fort",
        "Amboli Ghat": "Amboli Ghat",
        "Chikhaldara": "Chikhaldara",
        "Lonar Crater": "Lonar Crater",
        "Nashik Vineyards": "Nashik Vineyards",
        "Malshej Ghat": "Malshej Ghat",
        "Kalsubai Peak": "Kalsubai Peak",
        "Bhandardara": "Bhandardara",
        "Matheran": "Matheran",
        "Kaas Plateau": "Kaas Plateau",
        "Tadoba National Park": "Tadoba National Park",
        "Pench National Park": "Pench National Park",
        "Navegaon National Park": "Navegaon National Park",
        "Chandoli National Park": "Chandoli National Park",
        "Sanjay Gandhi National Park": "Sanjay Gandhi National Park",
        "Karnala Fort": "Karnala Fort",
        "Korlai Fort": "Korlai Fort",
        "Purandar Fort": "Purandar Fort",
        "Torna Fort": "Torna Fort",

        # New York
        "Statue of Liberty": "Statue of Liberty",
        "Brooklyn Bridge": "Brooklyn Bridge",
        "Empire State Building": "Empire State Building",
        "Central Park": "Central Park",
        "Times Square": "Times Square",
        "One World Trade Center": "One World Trade Center",
        "Rockefeller Center": "Rockefeller Center",
        "Metropolitan Museum of Art": "Metropolitan Museum of Art",
        "Grand Central Terminal": "Grand Central Terminal",
        "Ellis Island": "Ellis Island",
        "St. Patrick's Cathedral": "St. Patrick's Cathedral",
        "Carnegie Hall": "Carnegie Hall",
        "Flatiron Building": "Flatiron Building",
        "Radio City Music Hall": "Radio City Music Hall",
        "Wall Street": "Wall Street",
        "Chrysler Building": "Chrysler Building",
        "New York Public Library": "New York Public Library",
        "Broadway Theatre District": "Broadway Theatre District",
        "American Museum of Natural History": "American Museum of Natural History",
        "Federal Hall": "Federal Hall",
        "Solomon R. Guggenheim Museum": "Solomon R. Guggenheim Museum",
        "Bryant Park": "Bryant Park",
        "Madison Square Garden": "Madison Square Garden",
        "Cathedral of St. John the Divine": "Cathedral of St. John the Divine",
        "The High Line": "The High Line",
        "Coney Island": "Coney Island",
        "Prospect Park": "Prospect Park",
        "Brooklyn Botanic Garden": "Brooklyn Botanic Garden",
        "DUMBO": "DUMBO",
        "Williamsburg": "Williamsburg",
        "Green-Wood Cemetery": "Green-Wood Cemetery",
        "Flushing Meadows Park": "Flushing Meadows Park",
        "Queens Botanical Garden": "Queens Botanical Garden",
        "Jamaica Bay Wildlife Refuge": "Jamaica Bay Wildlife Refuge",
        "Fort Totten Park": "Fort Totten Park",
        "Pelham Bay Park": "Pelham Bay Park",
        "Van Cortlandt Park": "Van Cortlandt Park",
        "Wave Hill": "Wave Hill",
        "The Cloisters": "The Cloisters",
        "Roosevelt Island": "Roosevelt Island",
        "Governors Island": "Governors Island",
        "Snug Harbor Cultural Center": "Snug Harbor Cultural Center",
        "Staten Island Zoo": "Staten Island Zoo",
        "Fort Wadsworth": "Fort Wadsworth",
        "Socrates Sculpture Park": "Socrates Sculpture Park",
        "Gantry Plaza State Park": "Gantry Plaza State Park",
        "Hudson River Park": "Hudson River Park",
        "Battery Park": "Battery Park",
        "Little Island": "Little Island"
    }
    query = place_mapping.get(query, query)
    url = "https://en.wikipedia.org/w/api.php"
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
        st.warning(f"No image found for query: {query}")
        return None
    except Exception as e:
        st.error(f"Error fetching image: {e}")
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
            "Telangana": [
                "Golconda Fort", "Charminar", "Qutb Shahi Tombs", "Ramoji Film City", "Bhongir Fort",
                "Warangal Fort", "Thousand Pillar Temple", "Chowmahalla Palace", "Paigah Tombs",
                "Mecca Masjid", "Taramati Baradari", "Birla Mandir", "Medak Fort", "Kakatiya Kala Thoranam",
                "Salar Jung Museum", "Purani Haveli", "Falaknuma Palace", "Basar Saraswati Temple",
                "Khammam Fort", "Jadcherla Fort", "Elgandal Fort", "Kondapalli Fort", "Ananda Buddha Vihara",
                "Sri Raja Rajeshwara Temple", "Ghanpur Temples", "Pochampally", "Nizamabad Fort",
                "Kolanupaka Temple", "Alampur Temples", "Nagulapalli", "Pillalamarri", "Kaleshwaram Temple",
                "Yadagirigutta Temple", "Vemulawada Temple", "Bhadrachalam Temple", "Kulpakji Jain Temple",
                "Nalgonda Fort", "Mahabubnagar Fort", "Adilabad Fort", "Nirmal Fort", "Karimnagar Fort",
                "Sanghi Temple", "Dharmapuri Temple", "Jagtial Fort", "Manthani Temple", "Nizam Sagar",
                "Papi Hills", "Pakhal Lake", "Ramappa Temple", "Laknavaram Lake", "Kawal Wildlife Sanctuary"
            ],
            "Maharashtra": [
                "Gateway of India", "Ajanta Caves", "Ellora Caves", "Shaniwar Wada", "Raigad Fort",
                "Sinhagad Fort", "Daulatabad Fort", "Chhatrapati Shivaji Terminus", "Kanheri Caves",
                "Elephanta Caves", "Lohagad Fort", "Rajmachi Fort", "Pratapgad Fort", "Janjira Fort",
                "Pandavleni Caves", "Karla Caves", "Bhimashankar Temple", "Trimbakeshwar Temple",
                "Vikramshila University", "Bassein Fort", "Aurangabad Caves", "Harihar Fort",
                "Panhala Fort", "Tung Fort", "Sudhagad Fort", "Sindhudurg Fort", "Murud-Janjira Fort",
                "Kolhapur Palace", "Mahabaleshwar Temple", "Pratapgad Fort", "Ratnagiri Fort",
                "Vijaydurg Fort", "Amboli Ghat", "Chikhaldara", "Lonar Crater", "Nashik Vineyards",
                "Malshej Ghat", "Kalsubai Peak", "Bhandardara", "Matheran", "Kaas Plateau",
                "Tadoba National Park", "Pench National Park", "Navegaon National Park", "Chandoli National Park",
                "Sanjay Gandhi National Park", "Karnala Fort", "Korlai Fort", "Purandar Fort", "Torna Fort"
            ],
            "New York": [
                "Statue of Liberty", "Brooklyn Bridge", "Empire State Building", "Central Park",
                "Times Square", "One World Trade Center", "Rockefeller Center", "Metropolitan Museum of Art",
                "Grand Central Terminal", "Ellis Island", "St. Patrick's Cathedral", "Carnegie Hall",
                "Flatiron Building", "Radio City Music Hall", "Wall Street", "Chrysler Building",
                "New York Public Library", "Broadway Theatre District", "American Museum of Natural History",
                "Federal Hall", "Solomon R. Guggenheim Museum", "Bryant Park", "Madison Square Garden",
                "Cathedral of St. John the Divine", "The High Line", "Coney Island", "Prospect Park",
                "Brooklyn Botanic Garden", "DUMBO", "Williamsburg", "Green-Wood Cemetery", "Flushing Meadows Park",
                "Queens Botanical Garden", "Jamaica Bay Wildlife Refuge", "Fort Totten Park", "Pelham Bay Park",
                "Van Cortlandt Park", "Wave Hill", "The Cloisters", "Roosevelt Island", "Governors Island",
                "Snug Harbor Cultural Center", "Staten Island Zoo", "Fort Wadsworth", "Socrates Sculpture Park",
                "Gantry Plaza State Park", "Hudson River Park", "Battery Park", "Little Island"
            ]
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