import streamlit as st
st.header("Ticket Translator", divider="blue")

st.page_link("pages/Transport_Ticket_Hub.py", label="Transport Ticket Hub", icon="🚊")
st.write("Visit the Transport Ticket Hub for information on the transport authority in the state you're travelling to, including ticket types, how to use them and rules for the service.")
st.divider()
st.page_link("pages/Travel_Inspiration_Hub.py", label="Travel Inspiration Hub", icon="📍")
st.write("Visit the Travel Inspiration Hub for suggetsed travel locations depending on your destination, interests and the length of your trip")
st.divider()
st.page_link("pages/Question_Hub.py", label="Question Hub", icon="💬")
st.write("Want more information about transport or travel within Australia? Ask additional questions here!")
st.divider()