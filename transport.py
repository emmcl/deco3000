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
        generation_output = ""  # Store only the relevant 'new_generation' output
        for line in response.iter_lines():
            if line:
                content = json.loads(line.decode("utf-8"))
                value = content["value"]
                
                # Extract and store the 'new_generation' output
                if value["type"] == "outputs":
                    generation_output = value["values"].get("new_generation", "No generation found")
        
        # Display the 'new_generation' output in the Streamlit interface
        if generation_output:
            st.write(generation_output)
        else:
            st.warning("No valid generation found in the response.")

###############################################################################################################################

prompt_id = "06f26193-2a37-46c2-971c-c3a2b407b676"
load_dotenv()
api_key = os.getenv('API_KEY')

# Create a form
form = st.form("my_form")

# Input fields inside the form
location = form.text_input("Enter your location address")
start_date = form.date_input("Start Date")
end_date = form.date_input("End Date")

# Calculate the number of days between the dates
trip_length = None
if start_date and end_date:
    trip_length = str((end_date - start_date).days + 1)
else:
    st.write("Please select both start and end dates.")

# Add a submit button to the form
submit_button = form.form_submit_button("Submit")

# Prepare inputs only if the values are valid
if submit_button:
    if location and trip_length:
        inputs = {
            "Address": location,  # Changed from "Location" to "Address"
            "Trip Length": trip_length,
            "Prompt": f"Based on {location}, determine the name of the relevant transportation authority and the base URL for their public transport information."
        }

        # Call the API and display only the generation output
        wordware(inputs, prompt_id, api_key)
    else:
        st.warning("Please fill in the location and select valid start and end dates.")

