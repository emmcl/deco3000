import streamlit as st

# Initialize session state variables
if 'country' not in st.session_state:
    st.session_state['country'] = ""
if 'state' not in st.session_state:
    st.session_state['state'] = ""
if 'address' not in st.session_state:
    st.session_state['address'] = ""

# Create the form
with st.form("my_form"):
    # First question: Country selection
    st.session_state['country'] = st.selectbox(
        "Select a Country",
        ["", "Australia"],
    )
    st.session_state['state'] = st.selectbox(
        "Select a State",
        ["", "New South Wales", "Victoria", "ACT", "Queensland", 
            "Tasmania", "Western Australia", "South Australia", 
            "Northern Territory"],
    )

    # Initialize submit_button to None to avoid reference before assignment error
    submit_button = None

    if st.session_state['country'] == "Australia":
        # Second question: State selection
        st.session_state['state'] = st.selectbox(
            "Select a State",
            ["", "New South Wales", "Victoria", "ACT", "Queensland", 
             "Tasmania", "Western Australia", "South Australia", 
             "Northern Territory"],
        )

        if st.session_state['state']:
            # Third question: Enter address
            st.session_state['address'] = st.text_input("Enter your location street address")

            # Further questions only appear if an address has been entered
            if st.session_state['address']:
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                ticket_type = st.selectbox(
                    "Traveller Type",
                    ["Adult", "Student", "Senior/Pensioner"]
                )

                # Add a submit button to the form
                submit_button = st.form_submit_button("Submit")

# Display submitted data for debugging purposes
if submit_button:
    st.write("Country:", st.session_state['country'])
    st.write("State:", st.session_state['state'])
    st.write("Address:", st.session_state['address'])
    st.write("Start Date:", start_date)
    st.write("End Date:", end_date)
    st.write("Traveller Type:", ticket_type)