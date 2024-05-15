import streamlit as st
import requests
import json
import time

# Function to generate response from AskLLama model
def generate_response(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    history = []
    
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "AskLLama",
        "prompt": final_prompt,
        "stream": True  # Setting stream to True for continuous response
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=128):
            yield chunk.decode("utf-8")
    else:
        yield "ERROR: " + response.text

# Streamlit UI
st.set_page_config(page_title="Ask LLaMA", layout='centered', initial_sidebar_state='collapsed')
st.header("ASK LLaMA 🤖")

input_text = st.text_input("Enter the topic you want me to explain")

# Creating two more columns for additional two fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')

with col2:
    blog_style = st.selectbox('Writing the explanation for', ('Common People', 'Researchers', 'Data Scientist'), index=0)

submit = st.button("Generate")

# Display response
response_placeholder = st.empty()
full_response = ""

if submit:
    response_generator = generate_response(input_text)

    for chunk in response_generator:
        try:
            response_data = json.loads(chunk)
            response_text = response_data.get('response', '').strip()
            if response_text:
                full_response += response_text + "\n\n"  # Add paragraph break
                response_placeholder.text(full_response)
                time.sleep(0.05)  # Adjust sleep time for the desired speed of streaming
        except json.JSONDecodeError:
            # If the chunk is not valid JSON, simply display it
            response_placeholder.text(chunk)
