import streamlit as st

# Direct input elements without using a form
country = st.selectbox(
    "Select a Country",
    ["", "Australia"],
)

state = st.selectbox(
    "Select a State",
    ["", "New South Wales", "Victoria", "ACT", "Queensland", 
     "Tasmania", "Western Australia", "South Australia", 
     "Northern Territory"],
)

address = st.text_input("Enter your location street address")

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
ticket_type = st.selectbox(
    "Traveller Type",
    ["Adult", "Student", "Senior/Pensioner"]
)

# Add a submit button outside of the form
submit_button = st.button("Submit")

# Display submitted data
if submit_button:
    st.write("Country:", country)
    st.write("State:", state)
    st.write("Address:", address)
    st.write("Start Date:", start_date)
    st.write("End Date:", end_date)
    st.write("Traveller Type:", ticket_type)
