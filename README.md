# DECO3000 - Final Project
Kate Mander (kman6811) & Emma McLuckie (emcl8195)
- Project Link: https://github.com/emmcl/deco3000 

---

## Install
Ensure Python is installed. You can download it [here](https://www.python.org/downloads/).
We used:
- Python Version: 3.12.4 (base: conda)
- Streamlit Version: 1.38

In your terminal, install the necessary packages: 
- `pip install streamlit`
- `pip install python-dotenv`

## Clone the Project 
- `git clone https://github.com/emmcl/deco3000.git`

## API Keys
You will need to create a `.env` file in the root directory with the following:
- WORDWARE_API_KEY=your_key_here

- Kaz & Alton you'll find ours in a .txt file in the zip folder or you can use your own 
- But you will still need to make the .env file and paste it there

## Running The Program 
In your terminal: 
- `streamlit run Ticket_Translator.py`
- Note: This will open at a local host address, likely http://localhost:8501 

## Navigating The Program
Using the navigation bar or the buttons from the home page, you can access:
1. **Transport Ticket Hub** for information on the transport authority in the state you're travelling to. This includes ticket types, how to use them and rules for the service.
2. **Travel Inspiration Hub** for suggested travel locations based on your destination, interests, and the length of your trip.
3. **Question Hub** for more information about transport or travel within Australia? Ask additional questions here!

## Using the Program
Input your chosen values (within Australia) for each question and on submit Streamlit will output the Wordware response. 
- Please wait until the "Running" animation at the top of the screen has completed and disappeared, as this process can be slow.
 
