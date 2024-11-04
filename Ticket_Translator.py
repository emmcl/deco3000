import streamlit as st
st.header("Ticket Translator", divider="blue")

st.page_link("pages/Transport_Ticket_Hub.py", label="Transport Ticket Hub", icon="🚊")
st.write("Visit the Transport Ticket Hub for information on the transport authority in the state you're travelling to, including ticket types, how to use them and rules for the service.")
st.divider()
st.page_link("pages/Travel_Inspiration_Hub.py", label="Travel Inspiration Hub", icon="📍")
st.write("Visit the Travel Inspiration Hub for suggetsed travel locations depending on your destination and the length of your tri.p")
st.divider()
st.page_link("pages/Ask_A_Question.py", label="Ask A Question", icon="⁉️")
st.write("Have extra questions about transport or travel within Australia? Ask additional questions here!")
st.divider()