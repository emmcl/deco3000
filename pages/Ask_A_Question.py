import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
import json
import requests

st.page_link("Ticket_Translator.py", label=" Go Home", icon="🏠")
st.header("Ask A Question :heavy_exclamation_mark::question:", divider="blue")
    
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
prompt_id_chatbot = "f0be2817-61f3-4bc0-99d9-7cafe536829f"
# PROMPT:You are acting as a basic chatbot, using the location of @state in Australia. Find the relevant public transport authority and answer the @question from the user in 1-2 sentences.

form = st.form("form")

state = form.selectbox("Select a State", ["New South Wales", "Victoria", "ACT", "Queensland", "Tasmania", "Western Australia", "South Australia", "Northern Territory"], index=None, placeholder="e.g., New South Wales")
country = form.selectbox("Select a Country", ["Australia"], index=None, placeholder="e.g., Australia")
question = form.text_input("Enter your question", placeholder="e.g., What are the best places to visit?")
question_submit = form.form_submit_button("Submit")

if question_submit:
    inputs_chatbot = {
        "state": state,
        "country": country,
        "question": question
    }
    question_output = wordware(inputs_chatbot, prompt_id_chatbot, api_key)
    if question_output:
        st.subheader("To answer your question:")
        st.write(question_output)
    else:
        st.error("No response generated for the question.")