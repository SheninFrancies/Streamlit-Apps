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
st.title('Filters in Images')
st.text('This web application allows users to apply various filters on their images.')

file = 'Filters/Images/cover.jpg'
image = Image.open(file)
image = image.resize((500, 400))
col1, col2, col3 = st.columns(3)
col2.image(image)
