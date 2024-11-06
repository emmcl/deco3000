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
st.page_link("Ticket_Translator.py", label=" Go Home", icon="🏠")
st.header("Question Hub :speech_balloon:", divider="blue")

# set up streamilt form for user inputs 
form = st.form("form")
state = form.selectbox("Select a State", ["New South Wales", "Victoria", "Australian Capital Territory", "Queensland", "Tasmania", "Western Australia", "South Australia", "Northern Territory"], index=None, placeholder="eg. New South Wales")
country = form.selectbox("Select a Country", ["Australia"], index=None, placeholder="eg. Australia")
question = form.text_input("Enter your question", placeholder="eg., What are the best places to visit?")
submit_button = form.form_submit_button("Submit")

# prompt id to be given to wordware
prompt_id_chatbot = "4f2750ba-701a-4bc9-8b4c-8fed50dd2f92"

# on submit, set up variables for wordware function
if submit_button:

# set up variables for wordware function
    inputs_chatbot = {
        "state": state,
        "country": country,
        "question": question
    }
    # write output from wordware to the user
    question_output = wordware(inputs_chatbot, prompt_id_chatbot, api_key)
    if question_output:
        st.subheader("To answer your question:")
        st.write(question_output)
