import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
import json
import requests

# Load config.json
with open('config.json', 'r') as file:
    config = json.load(file)

# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv('WORDWARE_API_KEY')

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

prompt_id_recommendation = "38a4bff8-60c9-4498-9fcb-23146d64187e"  # First generation for ticket recommendation
prompt_id_use = "322d5421-8fba-4ac2-ae39-8b4e995c05b9"  # Second generation for ticket use
prompt_id_terms = "9d417150-c210-4151-9850-ad97a3bd0c56"  # Third generation for ticket use

# Create a form
form = st.form("my_form")

address = form.text_input("Enter your location street address", placeholder="e.g., 38 Princes Hwy, St Peters")
state = form.selectbox("Select a State", ["New South Wales", "Victoria", "ACT", "Queensland", "Tasmania", 
                                          "Western Australia", "South Australia", "Northern Territory"],
                       index=None, placeholder="e.g., New South Wales")
country = form.selectbox("Select a Country", ["Australia"], index=None, placeholder="e.g., Australia")
start_date = form.date_input("Start Date")
end_date = form.date_input("End Date")
travel_type = form.radio("Are you domestic or international?", ["Domestic", "International"], index=None)
ticket_type = form.radio("Traveller Type", ["Adult", "Student", "Senior"], index=None)
interests = form.text_input("What do you like doing?", placeholder="e.g., hiking, museums, restaurants")
planned_locations = form.text_input("Is there any specific destinations you have planned", 
                                    placeholder="e.g., SEALIFE Sydney Aquarium")

# Add a submit button to the form
submit_button = form.form_submit_button("Submit")

# Inside the submit button logic
if submit_button:
    images, ticket_names, ticket_machine_image = [], [], None

    # Retrieve images and ticket names based on config
    travel_key = travel_type.lower()
    ticket_key = ticket_type.lower()

    if state in config and travel_key in config[state] and ticket_key in config[state][travel_key]:
        images = config[state][travel_key][ticket_key]["images"]
        ticket_names = config[state][travel_key][ticket_key]["ticket_names"]
        ticket_machine_image = config[state]["ticket_machine_image"]
    else:
        st.error("Selection not found in config.")
    
    # Calculate trip length
    trip_length = None
    if start_date and end_date:
        trip_length = (end_date - start_date).days + 1
        if trip_length < 1:
            st.warning("End date should be after the start date.")
            trip_length = None
    else:
        st.warning("Please select both start and end dates.")

    # Prepare inputs for recommendation generation and display output
    if address and trip_length:
        inputs_recommendation = {
            "address": address,
            "state": state,
            "country": country,
            "trip_length": str(trip_length),
            "ticket_type": ticket_type,
            "travel_type": travel_type,
            "interests": interests,
            "planned_locations": planned_locations,
            "version": "^3.4"
        }

        # First generation: Ticket recommendation
        recommendation_output = wordware(inputs_recommendation, prompt_id_recommendation, api_key)
        if recommendation_output:
            st.write(recommendation_output)

            # Display images and captions only after the first generation output
            if images:
                st.image(images, caption=ticket_names, width=200)

        # Prepare inputs for ticket use generation
        inputs_use = {
            "address": address,
            "state": state,
            "country": country,
            "trip_length": str(trip_length),
            "ticket_type": ticket_type,
            "travel_type": travel_type,
            "interests": interests,
            "planned_locations": planned_locations,
            "version": "^3.4"
        }

        # Second generation: Ticket use
        use_output = wordware(inputs_use, prompt_id_use, api_key)
        if use_output:
            st.write(use_output)

            # Display ticket machine image after second generation output
            if ticket_machine_image:
                st.image(ticket_machine_image, caption="Ticket Activation Machine")

# Prepare inputs for ticket use generation
        inputs_terms = {
            "address": address,
            "state": state,
            "country": country,
            "trip_length": str(trip_length),
            "ticket_type": ticket_type,
            "travel_type": travel_type,
            "interests": interests,
            "planned_locations": planned_locations,
            "version": "^3.4"
        }

        # Second generation: Ticket use
        terms_output = wordware(inputs_terms, prompt_id_terms, api_key)
        if terms_output:
            st.write(terms_output)
    else:
        st.warning("Please fill in the location and select valid start and end dates.")
