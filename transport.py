import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import json
import requests 

###############################################################################################################################

'''
A GENERAL WORDWARE INTERFACE FUNCTION THAT HANDLES OUR POST REQUEST AND RESPONSE
This is based on the example from last week.
'''

def wordware(inputs, prompt_id, api_key):

    response = requests.post(
        f"https://app.wordware.ai/api/released-app/{prompt_id}/run",
        json={"inputs": inputs},
        headers={"Authorization": f"Bearer {api_key}"},
        stream=True,
    )

    if response.status_code != 200:
        print("Request failed with status code", response.status_code)
    else:
        # Successful api call
        for line in response.iter_lines():
            if line:
                content = json.loads(line.decode("utf-8"))
                value = content["value"]
                # We can print values as they're generated
                if value["type"] == "generation":
                    if value["state"] == "start":
                        print("\nNEW GENERATION -", value["label"])
                    else:
                        print("\nEND GENERATION -", value["label"])
                elif value["type"] == "chunk":
                    print(value["value"], end="")
                elif value["type"] == "outputs":
                    # Or we can read from the outputs at the end
                    # Currently we include everything by ID and by label - this will likely change in future in a breaking
                    # change but with ample warning
                    print("\nFINAL OUTPUTS:")
                    print(json.dumps(value, indent=4))

###############################################################################################################################

# Use streamlit to give us text and number inputs
# Create a form
form = st.form("my_form")

# Input fields inside the form
location = form.text_input("Enter your location address")
start_date = form.date_input("Start Date")
end_date = form.date_input("End Date")

# Add a submit button to the form
submitted = form.form_submit_button("Submit")

# Perform actions after form submission
if submitted:
    # Validate that a location is provided
    # if location:
    #     # Get transportation authority info from OpenAI
    #     # transport_info = 
    #     st.write(f"Transportation information for {location}: {transport_info}")
    # else:
        st.write("Please enter a location.")

# Calculate the number of days between the dates, including the final day
if start_date and end_date:
    delta_days = (end_date - start_date).days + 1
    st.write(f"The number of days for the trip is: {delta_days}")
else:
    st.write("Please select both start and end dates.")

# Display additional information
st.write(f"Trip duration: {delta_days} days")
st.write(f"location: {location}")


prompt_id = "06f26193-2a37-46c2-971c-c3a2b407b676"
# this is our course planning example from last week. Example inputs below:


# We need to grab our api-key from .env
load_dotenv()
api_key = os.getenv('API_KEY')

if location and start_date and end_date:
    st.write("Your inputs: ", location, start_date, end_date)
    inputs = {"Location": location, "start_date": start_date, "end_date": str(end_date)}
    result = st.button(
        "Submit",
        on_click=wordware,
        args=(
            inputs,
            prompt_id,
            api_key,
        ),
    )

