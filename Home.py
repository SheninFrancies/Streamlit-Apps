import streamlit as st
from PIL import Image

st.set_page_config(layout='wide', page_title='Card Validity Checker')

# Remove Footer and Menu
hide_footer = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility:hidden;}
    </style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

# Title and Intro
st.title('Card Validity Checker')
st.text('This web application allows users to check the validity of their Credit Card or Driving License.')
st.text('The validity is checked by employing the concept of OCR in OpenCV.')

file = "CardValidity/Images/home_image.jpg"
image = Image.open(file)
st.image(image)
