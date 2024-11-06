import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
import json
import requests

# define the wordware function 
def wordware(inputs, prompt_id, api_key):
    try:
        response = requests.post(
            f"https://app.wordware.ai/api/released-app/{prompt_id}/run",
            json={"inputs": inputs},
            headers={"Authorization": f"Bearer {api_key}"},
            stream=True,
        )
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to make request: {e}")
        return None

    if response.status_code != 200:
        st.error(f"Request failed with status code {response.status_code}: {response.text}")
        return None
    else:
        final_output = None
        # Check if content is NDJSON
        if response.headers.get('Content-Type') == 'application/x-ndjson; charset=utf-8':
            for line in response.iter_lines():
                if line:
                    try:
                        content = json.loads(line.decode("utf-8"))
                        value = content["value"]
                        if value["type"] == "outputs":
                            final_output = value["values"].get("new_generation", "No generation found")
                    except json.JSONDecodeError:
                        st.error("Error decoding NDJSON response.")
        return final_output

# load environment variables from the .env file to get API KEY 
# for this submission you can find the WORDWARE_API_KEY in a .txt file in the .zip folder or use your own
load_dotenv()
api_key = os.getenv('WORDWARE_API_KEY')

# heading and link back to home for navigation
st.page_link("Ticket_Translator.py", label="Go Home", icon="🏠")
st.header("Travel Inspiration Hub :round_pushpin:", divider="blue")

# set up streamilt form for user inputs 
form = st.form("my_form")
address = form.text_input("Enter your location street address", placeholder="eg. 1 Main Street, Sydney")
state = form.selectbox("Select a State", ["New South Wales", "Victoria", "Australian Capital Territory", "Queensland", "Tasmania", "Western Australia", "South Australia", "Northern Territory"], index=None, placeholder="eg. New South Wales")
country = form.selectbox("Select a Country", ["Australia"], index=None, placeholder="eg. Australia")
start_date = form.date_input("Start Date")
end_date = form.date_input("End Date")
planned_locations = form.text_input("Is there any specific destinations you have planned", placeholder="eg. SEALIFE Sydney Aquarium")
interests = form.text_input("What do you like doing?", placeholder="eg. hiking, museums, restaurants")
submit_button = form.form_submit_button("Submit")

# prompt id to be given to wordware
prompt_id_recommendation = "acea7b7a-141b-4982-bc48-b2a71c4b13a1" 

# on submit, set up variables for wordware function
if submit_button:
    # Calculate trip length
    trip_length = None
    if start_date and end_date:
        trip_length = (end_date - start_date).days + 1
        if trip_length < 1:
            st.warning("End date should be after the start date.")
            trip_length = None
    else:
        st.warning("Please select both start and end dates.")

    # set up variables for wordware function
    inputs = {
        "address": address,
        "state": state,
        "country": country,
        "trip_length": str(trip_length),
        "interests": interests,
        "planned_locations": planned_locations,
        "version": "^3.4"
    }

    recommendation_output = wordware(inputs, prompt_id_recommendation, api_key)
    if recommendation_output:
        st.write(recommendation_output)

# link to chatbot 
st.page_link(label="If you need more help... ask a question here!", page="pages/Question_Hub.py", icon="⁉️")
