import streamlit as st
from NLP import start
import time

start_ = start()
intro_message = """Hello I'm a doctors appointment managing chatbot. I can help you with 
booking, editing and cancelling your appointments. Along with this I can also get information
about already booked appointments.

How can I help you today ?"""

st.title("Doctors appointment managing assistant")

if "stage" not in st.session_state:
    st.session_state.stage = start_.intent_classifier

if "history" not in st.session_state:
    st.session_state.history = []
    with st.chat_message("assistant"):
        st.markdown(intro_message)
    st.session_state.history.append({"role": "assistant", "content": intro_message})
    



user_input = st.chat_input("Enter your text here")


if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    response, st.session_state.stage = st.session_state.stage(user_input)
    st.session_state.history.append({"role": "assistant", "content": response})
    
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        