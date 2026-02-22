from dotenv import load_dotenv 
import os 
from PIL import Image 
import google.generativeai as genai 
import streamlit as st 


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(prompt,image,input):
    model=genai.GenerativeModel('gemini-3-flash-preview')
    response=model.generate_content([input,image,prompt])
    return response.text 


def input_image_setup(uploaded_image):
    if uploaded_image is not None:
        bytes_data=uploaded_image.getvalue()
        image_parts=[
            {
                'mime_data':uploaded_image.type,
                'data':bytes_data 
            }
        ]
        return image_parts 
    else:
        raise FileNotFoundError("No file found")
    

st.set_page_config(page_title='Gemini INVOICE extractor')
st.header('Gemini APP')
input=st.text_input("Input your query",key='input')
uploaded_file=st.file_uploader('Choose an image ...',type=["jpg",'jpeg','png'])
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image)

submit=st.button("Tell me about this image")

input_prompt="""
You are an expert in understanding invoices.
You will receive the image of an invoice and you will have to answer questions based on it 

"""
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image,input)
    st.subheader("Answer: ")
    st.write(response)
