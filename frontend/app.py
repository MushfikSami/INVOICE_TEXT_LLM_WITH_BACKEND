import streamlit as st 
import requests 
from PIL import Image 
import os 


BACKEND_URL=os.getenv("BACKEND_URL","http://localhost:8000")
API_TOKEN=os.getenv('API_TOKEN')


st.set_page_config(page_title='GEMINI IMAGE DATA EXTRACTOR')
st.header("GEMINI APP")

input=st.text_input("Input Your Query",key='input',value='You are an expert in reading invoices. Read this invoice and Answer my questions')
uploaded_file=st.file_uploader('Choose an image...',type=['jpeg','jpg','png'])



if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image)

if st.button('ASK'):
    if uploaded_file and input:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        data = {"prompt": input}
        headers = {"x-api-token": os.getenv("API_TOKEN")}
        
        with st.spinner("Extracting data via backend..."):
            response = requests.post("http://fastapi_backend:8000/extract", files=files, data=data, headers=headers)
            
            # Check if the backend was successful
            if response.status_code == 200:
                result = response.json()
                st.success(f"Response fetched from: **{result['source']}**")
                st.write(result["answer"])
            else:
                # If it's a 500 error, print the error detail!
                error_msg = response.json().get("detail", "Unknown Backend Error")
                st.error(f"Backend Error {response.status_code}: {error_msg}")
    else:
        st.warning("Please upload an image and enter a query.")