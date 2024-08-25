import streamlit as st
from inference import Inference

# Initialize the Inference class
inference = Inference()

# Streamlit app layout
st.title('Agent Recommender')

with st.chat_message('assistant'):
    st.write("Hi!, I am Lyra. How can I help you")

# Initialize session state for storing messages
if "user_messages" not in st.session_state:
    st.session_state.user_messages = []
if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []

# Display previous messages
if st.session_state.user_messages:
    for i in range(max(len(st.session_state.user_messages), len(st.session_state.assistant_responses))):
        if i < len(st.session_state.user_messages):
            with st.chat_message("user"):
                st.markdown(st.session_state.user_messages[i])
        if i < len(st.session_state.assistant_responses):
            with st.chat_message("assistant"):
                st.markdown(st.session_state.assistant_responses[i])

# Input text box for the query
user_query = st.chat_input("Your message:")

if user_query and user_query.strip() != "":
    with st.chat_message('user'):
        st.markdown(user_query)
    st.session_state.user_messages.append(user_query)

    # Get the response from the custom query engine
    response = inference._query_engine(user_query)
    st.session_state.assistant_responses.append(response)

    with st.chat_message('assistant'):
        st.markdown(response)
