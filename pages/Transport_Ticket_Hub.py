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

# load config.json
with open('config.json', 'r') as file:
    config = json.load(file)
    
# heading and link back to home for navigation
st.page_link("Ticket_Translator.py", label=" Go Home", icon="🏠")
st.header("Transport Ticket Hub :tram:", divider="blue")

# set up streamilt form for user inputs 
form = st.form("my_form")
state = form.selectbox("Select a State", ["New South Wales", "Victoria", "Australian Capital Territory", "Queensland", "Tasmania", "Western Australia", "South Australia", "Northern Territory"], index=None, placeholder="eg., New South Wales")
country = form.selectbox("Select a Country", ["Australia"], index=None, placeholder="eg. Australia")
travel_type = form.radio("Are you domestic or international?", ["Domestic", "International"], index=None)
ticket_type = form.radio("Traveller Type", ["Adult", "Student", "Senior"], index=None)
submit_button = form.form_submit_button("Submit")

# prompt id - first generation for ticket recommendation
prompt_id_recommendation = "38a4bff8-60c9-4498-9fcb-23146d64187e" 
# prompt id - second generation for ticket use
prompt_id_use = "322d5421-8fba-4ac2-ae39-8b4e995c05b9"  
# prompt id - third generation for ticket terms
prompt_id_terms = "9d417150-c210-4151-9850-ad97a3bd0c56"  

# on submit, set up variables for wordware function
if submit_button:
    # retrieve ticket_images and ticket names based on config
    ticket_images, ticket_names, ticket_machine_image = [], [], None
    travel_key = travel_type.lower()
    ticket_key = ticket_type.lower()

    if state in config and travel_key in config[state] and ticket_key in config[state][travel_key]:
        ticket_images = config[state][travel_key][ticket_key]["ticket_images"]
        ticket_names = config[state][travel_key][ticket_key]["ticket_names"]
        ticket_machine_image = config[state]["ticket_machine_image"]
    else:
        st.error("Selection not found in config.")
    
# set up variables for wordware function
    inputs = {
        "state": state,
        "country": country,
        "ticket_type": ticket_type,
        "travel_type": travel_type,
        "version": "^3.4"
    }

    # first generation: ticket recommendation
    recommendation_output = wordware(inputs, prompt_id_recommendation, api_key)
    if recommendation_output:
        st.write(recommendation_output)
        # display ticket_images and captions from config.JSON
        if ticket_images:
            st.image(ticket_images, caption=ticket_names, width=200)

    # second generation: ticket use
    use_output = wordware(inputs, prompt_id_use, api_key)
    if use_output:
        st.write(use_output)
        # display ticket machine image from config.JSON
        if ticket_machine_image:
            st.image(ticket_machine_image, caption="Ticket Activation Machine")

    # third generation: ticket terms
    terms_output = wordware(inputs, prompt_id_terms, api_key)
    if terms_output:
        st.write(terms_output)

# link to chatbot 
st.page_link(label="If you need more help... ask a question here!", page="pages/Question_Hub.py", icon="⁉️")
