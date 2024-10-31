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
    response = requests.post(
        f"https://app.wordware.ai/api/released-app/{prompt_id}/run",
        json={"inputs": inputs},
        headers={"Authorization": f"Bearer {api_key}"},
        stream=True,
    )

    if response.status_code != 200:
        try:
            st.error(f"Request failed with status code {response.status_code}: {response.text}")
        except ValueError:
            st.error(f"Request failed with status code {response.status_code}.")
    else:
        final_output = None
        
        # Check if content is NDJSON
        if response.headers.get('Content-Type') == 'application/x-ndjson; charset=utf-8':
            # Process NDJSON lines
            for line in response.iter_lines():
                if line:
                    try:
                        # Each line is a valid JSON object
                        content = json.loads(line.decode("utf-8"))
                        value = content["value"]

                        if value["type"] == "outputs":
                            final_output = value["values"].get("new_generation", "No generation found")
                    except json.JSONDecodeError:
                        st.error("Error decoding NDJSON response.")
        
        # Display the result in the Streamlit interface if available
        if final_output:
            st.write(final_output)
        else:
            st.warning("No valid generation found in the response.")

prompt_id = "a201c977-e13a-4f2b-b7a3-3f47acdcfbd2"

# Create a form
form = st.form("my_form")

address = form.text_input("Enter your location street address", 
    placeholder="eg. 38 Princes Hwy, St Peters")

state = form.selectbox(
    "Select a State",
    ["New South Wales", "Victoria", "ACT", "Queensland", 
     "Tasmania", "Western Australia", "South Australia", 
     "Northern Territory"],
    index=None,
    placeholder="eg. New South Wales"
)

country = form.selectbox(
    "Select a Country",
    ["Australia"],
    index=None,
    placeholder="eg. Australia"
)

start_date = form.date_input("Start Date")
end_date = form.date_input("End Date")

travel_type = form.radio(
    "Are you domestic or internation?",
    ["Domestic", "International"], 
    index=None
)

ticket_type = form.radio(
    "Traveller Type",
    ["Adult", "Student", "Senior"],
    index=None
)

interests = form.text_input("What do you like doing?", 
    placeholder="eg. hiking, museums, restaurants")

planned_locations = form.text_input("Is there any specific destinations you have planned", 
    placeholder="eg. SEALIFE Sydney Aquarium")

ticket_name = "Opal"

# Add a submit button to the form
submit_button = form.form_submit_button("Submit")
# Display submitted data
if submit_button:


    images = []
    ticket_names = []
        # Ensure state has a valid value before accessing config
    if state:
        if state in config:
            # Nested conditions to access travel type and ticket type
            if travel_type.lower() in config[state]:
                if ticket_type.lower() in config[state][travel_type.lower()]:
                    images = config[state][travel_type.lower()][ticket_type.lower()]["images"]
                    ticket_names = config[state][travel_type.lower()][ticket_type.lower()]["ticket_names"]
                else:
                    st.error(f"Ticket type '{ticket_type}' not found in '{travel_type}' for state '{state}'.")
            else:
                st.error(f"Travel type '{travel_type}' not found for state '{state}'.")
        else:
            st.error(f"State '{state}' not found in config.")
    else:
        st.warning("Please select a valid state.")

    if images:
        st.image(images, caption=ticket_names,  width=200)



# Calculate the number of days between the dates
trip_length = None
if start_date and end_date:
    trip_length = str((end_date - start_date).days + 1)
else:
    st.write("Please select both start and end dates.")




# Prepare inputs only if the values are valid
if submit_button:
    # Check if country and state are valid selections
    if country == "Select a country" or state in ["Select a state", "Select a region"]:
        st.warning("Please select a valid country and state/region.")
    # Check if location and trip length are provided
    elif address and trip_length:
        if address.strip() == "" or trip_length.strip() == "":
            st.error("Location or trip length cannot be empty.")
        else:
            inputs = {
                # i think we should change this to address instead of location
                "address": address,
                "state": state,
                "country": country,
                "trip_length": trip_length,
                "ticket_type": ticket_type,
                "travel_type": travel_type,
                "interests": interests,
                "planned_locations": planned_locations,
                "ticket_name": ticket_name,
                "version": "^3.4"  # Add the version information here

            }
            # Call the API and display the generation output
            wordware(inputs, prompt_id, api_key)
    else:
        st.warning("Please fill in the location and select valid start and end dates.")









