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
        for line in response.iter_lines():
            if line:
                content = json.loads(line.decode("utf-8"))
                value = content["value"]
                if value["type"] == "generation":
                    if value["state"] == "start":
                        st.write("\nNEW GENERATION -", value["label"])
                    else:
                        st.write("\nEND GENERATION -", value["label"])
                elif value["type"] == "chunk":
                    st.write(value["value"], end="")
                elif value["type"] == "outputs":
                    st.write("\nFINAL OUTPUTS:")
                    st.json(value)

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
    st.write(f"The number of days for the trip is: {trip_length}")
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

        st.write("Sending the following inputs to the API:")
        st.json(inputs)  # Log the inputs for debugging
        wordware(inputs, prompt_id, api_key)  # Call the API
    else:
        st.warning("Please fill in the location and select valid start and end dates.")

# Display additional information
if trip_length:
    st.write(f"Trip duration: {trip_length} days")
if location:
    st.write(f"Location: {location}")

if location and start_date and end_date:
    st.write("Your inputs:", location, start_date, end_date)
