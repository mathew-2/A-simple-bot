import streamlit as st
import requests

st.set_page_config(page_title="A chatbot", page_icon="🦖", layout="wide")
st.title('A simple chatbot 🤖 ')

txt = st.text_area(
    "Text to analyze",
    "It was the best of times, it was the worst of times, it was the age of "
    "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    "was the epoch of incredulity, it was the season of Light, it was the "
    "season of Darkness, it was the spring of hope, it was the winter of despair, (...)",
)

if st.button("Get Chatbot's Verdict"):
    lambda_url = "https://h3gkodisi2rg4ubeaxnr4ztps40getip.lambda-url.us-east-1.on.aws/"
    
    # Print the data being sent to Lambda
    print(f"Sending data to Lambda: {txt}")
    
    # Send the data as JSON payload with the key 'prompt'
    payload = {"prompt": txt}
    
    response = requests.post(lambda_url, json=payload)
    
    if response.status_code == 200:
        st.subheader("Chatbot's verdict:")
        
        # Print the response from Lambda
        print(f"Received from Lambda: {response.json()}")
        
        st.write(response.json().get('outputText', ''))
    
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
