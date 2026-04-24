import streamlit as st
import requests

st.title("Conversational Analytics Demo")

question = st.text_input("Ask a question")

if st.button("Submit"):
    res = requests.post("http://localhost:8000/query", json={"question": question})
    st.json(res.json())
