import openai  # Correct import for the openai library
import streamlit as st

st.title("ChatGPT-like clone")

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Call the OpenAI API using the correct method
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        # Stream and display the response
        collected_response = ""
        for chunk in response:
            content_chunk = chunk['choices'][0]['delta'].get('content', '')
            collected_response += content_chunk
            st.write(content_chunk, end="")

        # Append the full response to the session state
        st.session_state.messages.append({"role": "assistant", "content": collected_response})
