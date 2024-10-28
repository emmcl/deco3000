import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
import json
import requests

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

prompt_id = "06f26193-2a37-46c2-971c-c3a2b407b676"

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

ticket_type = form.radio(
    "Traveller Type",
    ["Adult", "Student", "Senior/Pensioner"]
)

international_domestic = form.radio(
    "Are you domestic or internation?",
    ["Domestic", "International"]
)

interests = form.text_input("What do you like doing?", 
    placeholder="eg. hiking, museums, restaurants")
planned_locations = form.text_input("Is there any specific destinations you have planned", 
    placeholder="eg. SEALIFE Sydney Aquarium")

# Add a submit button to the form
submit_button = form.form_submit_button("Submit")
# Display submitted data
if submit_button:
    st.write("Address:", address)
    st.write("State:", state)
    st.write("Country:", country)
    st.write("Start Date:", start_date)
    st.write("End Date:", end_date)
    st.write("Traveller Type:", ticket_type)
    st.write("International or Domestic:", international_domestic)

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
                "version": "^3.4"  # Add the version information here

            }
            # Call the API and display the generation output
            wordware(inputs, prompt_id, api_key)
    else:
        st.warning("Please fill in the location and select valid start and end dates.")


# Google Custom Search API details
load_dotenv()
GOOGLE_API_KEY  = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = 'd212ba4f3a000451c'





def get_image_url(state):
    # Modify the query to be more specific
    # specific_query = f"public transport tickets for {state} in {country} in 2024"
    # specific_query = f"{state} public transport card"
    specific_query = f"transport {state} travel card"
    url = f"https://www.googleapis.com/customsearch/v1?q={specific_query}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}&searchType=image&num=1"
    
    # Send request to Google Custom Search API
    response = requests.get(url)
    data = response.json()
    
    # Extract the image URL from the search results
    if 'items' in data:
        image_url = data['items'][0]['link']
        return image_url
    else:
        return None

if submit_button:
    if state:        
        # Get the image URL
        image_url = get_image_url(state)
        
        if image_url:
            # Display the image
            st.subheader(f"{state} Transport Ticketing System", divider="gray")
            st.image(image_url, caption=f"Image of {state}", use_column_width=True)
        else:
            st.write("No image found for the location.")

