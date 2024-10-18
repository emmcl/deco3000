import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
import json
import requests

###############################################################################################################################

def wordware(inputs, prompt_id, api_key):
    response = requests.post(
        f"https://app.wordware.ai/api/released-app/{prompt_id}/run",
        json={"inputs": inputs},
        headers={"Authorization": f"Bearer {api_key}"},
        stream=True,
    )

    if response.status_code != 200:
        st.error(f"Request failed with status code {response.status_code}: {response.text}")
    else:
        generation_output = ""
        for line in response.iter_lines():
            if line:
                content = json.loads(line.decode("utf-8"))
                value = content["value"]
                
                if value["type"] == "outputs":
                    generation_output = value["values"].get("new_generation", "No generation found")
        
        if generation_output:
            st.write(generation_output)
        else:
            st.warning("No valid generation found in the response.")

###############################################################################################################################

prompt_id = "2f6baa39-f896-471b-ad07-12711141cfc1"
load_dotenv()
api_key = os.getenv('API_KEY')

# Create a form
form = st.form("my_form")

# Input fields inside the form
location = form.text_input("Enter your location address")
start_date = form.date_input("Start Date")
end_date = form.date_input("End Date")

# Add a submit button to the form
submit_button = form.form_submit_button("Submit")

# Check form submission
if submit_button:
    # Ensure both location and date range are provided
    if location and start_date and end_date:
        # Calculate the trip length
        trip_length = (end_date - start_date).days + 1
        
        # Prepare the inputs for the API with correct keys
        inputs = {
            "location": location.strip(),  # Key for location
            "trip_length": str(trip_length),  # Key for trip length
            "Prompt": f"Based on {location.strip()}, determine the name of the relevant transportation authority and the base URL for their public transport information."
        }

        # Debug statement to check what is being sent
        st.write(f"Inputs being sent to API: {inputs}")

        # Call the API
        wordware(inputs, prompt_id, api_key)
    else:
        st.warning("Please enter a location and select valid start and end dates.")
