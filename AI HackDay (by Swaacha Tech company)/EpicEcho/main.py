import streamlit as st
import google.generativeai as genai
import requests
import api_keys

# Configure Gemini API
GEMINI_API_KEY = api_keys.gemini_api  # Your Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Function to fetch an image of a historical place using Wikimedia Commons API
def fetch_wikimedia_image(place_name):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": place_name,
        "srnamespace": "6",  # Search only in the file namespace (images)
        "srlimit": "1"  # Fetch only the first result
    }
    response = requests.get(url, params=params).json()
    
    if response.get("query", {}).get("search"):
        page_title = response["query"]["search"][0]["title"]
        image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{page_title.replace(' ', '_')}"
        return image_url
    return None

# Function to generate a list of historical places in a given state
def generate_historical_places(state):
    try:
        prompt = f"List the top 5 most famous historical places in {state}, India. Provide only the names, separated by commas."
        response = model.generate_content(prompt)
        return response.text.split(", ")
    except Exception as e:
        st.warning(f"API quota exhausted or error occurred: {e}. Using fallback data.")
        return FALLBACK_DATA.get(state, []) # type: ignore

# Function to generate a compelling narrative using Gemini API
def generate_narrative(place_name, state):
    try:
        prompt = f"Write a compelling narrative about the historical significance of {place_name} in {state}, India, in 100 words."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate narrative due to API error: {e}"

# Function to generate facts about a historical place using Gemini API
def generate_facts(place_name, state):
    try:
        prompt = f"Provide 2 interesting historical facts about {place_name} in {state}, India."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate facts due to API error: {e}"

# Function to generate traffic information using Gemini API
def generate_traffic_info(place_name, state):
    try:
        prompt = f"Provide traffic information for visitors to {place_name} in {state}, India. Include peak hours and recommendations."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate traffic info due to API error: {e}"

# Streamlit App
def main():
    st.title("AI-Powered Historical Places Chatbot")
    st.write("Discover fascinating historical places in India with compelling narratives!")

    # User input
    country = st.selectbox("Select Country", ["India"])
    state = st.selectbox("Select State", ["Telangana", "Maharashtra"])

    if st.button("Get Historical Places"):
        # Generate a list of historical places in the given state
        historical_places = generate_historical_places(state)
        
        if historical_places:
            st.subheader(f"Historical Places in {state}, {country}")
            for place_name in historical_places:
                st.markdown("---")
                st.subheader(place_name)

                # Generate and display narrative
                narrative = generate_narrative(place_name, state)
                st.write(f"📖 **Narrative:** {narrative}")

                # Generate and display facts
                facts = generate_facts(place_name, state)
                st.write("📜 **Facts:**")
                st.write(facts)

                # Generate and display traffic information
                traffic_info = generate_traffic_info(place_name, state)
                st.write(f"🚶 **Traffic Info:** {traffic_info}")

                # Fetch and display image from Wikimedia Commons
                image_url = fetch_wikimedia_image(place_name)
                if image_url:
                    st.image(image_url, caption=f"Image of {place_name}")
                else:
                    st.write("🖼️ **Image not available**")

                # Simulate location (using Gemini API)
                location_prompt = f"Provide the location of {place_name} in {state}, India."
                try:
                    location_response = model.generate_content(location_prompt)
                    st.write(f"📍 **Location:** {location_response.text}")
                except Exception as e:
                    st.write(f"📍 **Location:** Could not fetch location due to API error: {e}")
        else:
            st.error("No historical places found for the given state.")

if __name__ == "__main__":
    main()