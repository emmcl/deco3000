import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
import json
import requests


# Load config.json
with open('config.json', 'r') as file:
    config = json.load(file)
    
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

# Load environment variables from the .env file to get API KEY 
load_dotenv()
api_key = os.getenv('WORDWARE_API_KEY')

# Create a form
form = st.form("my_form")

address = form.text_input("Enter your location street address", placeholder="e.g., 38 Princes Hwy, St Peters")
state = form.selectbox("Select a State", ["New South Wales", "Victoria", "ACT", "Queensland", "Tasmania", "Western Australia", 
                                          "South Australia", "Northern Territory"], index=None, placeholder="e.g., New South Wales")
country = form.selectbox("Select a Country", ["Australia"], index=None, placeholder="e.g., Australia")
start_date = form.date_input("Start Date")
end_date = form.date_input("End Date")
travel_type = form.radio("Are you domestic or international?", ["Domestic", "International"], index=None)
ticket_type = form.radio("Traveller Type", ["Adult", "Student", "Senior"], index=None)
planned_locations = form.text_input("Is there any specific destinations you have planned", placeholder="e.g., SEALIFE Sydney Aquarium")
interests = form.text_input("What do you like doing?", placeholder="e.g., hiking, museums, restaurants")

# Add a submit button to the form
submit_button = form.form_submit_button("Submit")

# Inside the submit button logic
if submit_button:
    ticket_images =[]
    ticket_names = []
    ticket_machine_image = None
    # Retrieve ticket_images and ticket names based on config
    travel_key = travel_type.lower()
    ticket_key = ticket_type.lower()

    if state in config and travel_key in config[state] and ticket_key in config[state][travel_key]:
        ticket_images = config[state][travel_key][ticket_key]["ticket_images"]
        print(ticket_images)
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


    # store values for the fake chatbot 
    st.session_state.address = address
    st.session_state.state = state
    st.session_state.country = country
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date
    st.session_state.travel_type = travel_type
    st.session_state.ticket_type = ticket_type
    st.session_state.planned_locations = planned_locations
    st.session_state.interests = interests

    # Retrieve ticket_images and ticket names based on config
    travel_key = travel_type.lower()
    ticket_key = ticket_type.lower()
# Retrieve ticket_images and ticket names based on config and store in session state
    if state in config and travel_key in config[state] and ticket_key in config[state][travel_key]:
        # Store values in session state
        st.session_state.ticket_images = config[state][travel_key][ticket_key]["ticket_images"]
        st.session_state.ticket_names = config[state][travel_key][ticket_key]["ticket_names"]
        st.session_state.ticket_machine_image = config[state]["ticket_machine_image"]
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
    inputs = {
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
      
    prompt_id_recommendation = "38a4bff8-60c9-4498-9fcb-23146d64187e"  # First generation for ticket recommendation
    prompt_id_use = "322d5421-8fba-4ac2-ae39-8b4e995c05b9"  # Second generation for ticket use
    prompt_id_terms = "9d417150-c210-4151-9850-ad97a3bd0c56"  # Third generation for ticket use
    prompt_id_chatbot = "f0be2817-61f3-4bc0-99d9-7cafe536829f" # Fourth generation - faking a chat bot

    # wordware generations
    recommendation_output = wordware(inputs, prompt_id_recommendation, api_key)
    use_output = wordware(inputs, prompt_id_use, api_key)
    terms_output = wordware(inputs, prompt_id_terms, api_key)
    
    if recommendation_output:
        st.session_state.recommendation_output = recommendation_output # store in session state 
    if use_output:
        st.session_state.use_output = use_output  # Store in session state
    if terms_output:
        st.session_state.terms_output = terms_output  # Store in session state

# Check if there's a stored output for recommendation and display it
if 'recommendation_output' in st.session_state:
    st.write("Ticket Recommendation:")
    st.write(st.session_state.recommendation_output)
if ticket_images:
    st.image(ticket_images, caption=ticket_names, width=200)  
# Check if there's a stored output for use and display it
if 'use_output' in st.session_state:
    st.write("Ticket Use Information:")
    st.write(st.session_state.use_output)
if ticket_machine_image:
    st.image(ticket_machine_image, caption="Ticket Activation Machine")
# Check if there's a stored output for terms and display it
if 'terms_output' in st.session_state:
    st.write("Terms and Conditions:")
    st.write(st.session_state.terms_output)

# retrieving session state values 
previous_address = st.session_state.get('address', '')
previous_state = st.session_state.get('state', '')
previous_country = st.session_state.get('country', '')
previous_start_date = st.session_state.get('start_date', '')
previous_end_date = st.session_state.get('end_date', '')
previous_travel_type = st.session_state.get('travel_type', '')
previous_ticket_type = st.session_state.get('ticket_type', '')
previous_planned_locations = st.session_state.get('planned_locations', '')
previous_interests = st.session_state.get('interests', '')

    # potential chatbot
st.page_link(label="Need more help.. Ask a question here", page="pages/question_page")

    # Instead of processing here, navigate to another page
    # st.session_state.user_question = st.text_input("Enter your question", placeholder="e.g., What are the best places to visit.")
    