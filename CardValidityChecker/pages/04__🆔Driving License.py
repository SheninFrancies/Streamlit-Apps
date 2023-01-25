import streamlit as st
import io
import numpy as np
from PIL import Image
import cv2
import pytesseract
from pytesseract import Output
import re
import dateutil
import arrow

st.set_page_config(layout='wide', page_title='Driving License')

# Remove Footer and Menu
hide_footer = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility:hidden;}
    </style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

# Sidebar Setup
st.sidebar.title('Select a File')
uploaded_file = st.sidebar.file_uploader('Upload an Image of the Driving License',  type=['jpg', 'png'])

# Title and Intro
if uploaded_file is None:
    st.title('Driving License Validity Checker')
    st.text('Explore this page to check the validity of the Driving License.')


# Convert Image
def save_image(byteImage):
    bytesImg = io.BytesIO(byteImage)
    imgFile = Image.open(bytesImg)
    return imgFile


## Preprocess the Image
def image_preprocessing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


## Get the Dates
def get_card_data(image_preprocessed):
    data = pytesseract.image_to_data(image_preprocessed,output_type=Output.DICT)
    date_pattern = ["^[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}$", "^[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}$",
                    "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"]
    n_boxes = len(data['text'])
    extract = []
    for i in range(n_boxes):
        for j in date_pattern:
            if data['conf'][i] > 10:
                if re.match(j, data['text'][i]):
                    extract.append(data['text'][i])
    return extract

# Check Validity
def get_card_validity(extract):
    dates = []
    for date in extract:
        if '.' in date:
            date = arrow.get(date, 'DD.MM.YYYY').date()
            dates.append(date)
        elif '-' in date:
            date = arrow.get(date, 'DD-MM-YYYY').date()
            dates.append(date)
        elif '/' in date:
            date = arrow.get(date, 'DD/MM/YYYY').date()
            dates.append(date)

    valid_date = max(dates)
    current_date = arrow.utcnow().date()
    if current_date > valid_date:
        validity_period = dateutil.relativedelta.relativedelta(current_date, valid_date)
        license_validity = 'Driving License is **INVALID** and is {} years, {} months and {} days past the validity.'.format(validity_period.years, validity_period.months, validity_period.days)
    else:
        validity_period = dateutil.relativedelta.relativedelta(valid_date, current_date)
        license_validity = 'Driving License is **VALID** and the validity ends in {} years, {} months and {} days.'.format(validity_period.years, validity_period.months, validity_period.days)
    return license_validity, valid_date


# Check if the file has been uploaded
if uploaded_file is not None:
    file = uploaded_file.read()
    path = save_image(file)
    st.title('Driving License Validity Checker')
    st.markdown('## Original Driving License')
    st.image(path, width=500, caption='Original Driving License')
    file_bytes = np.asarray(bytearray(file), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    gray_image = image_preprocessing(opencv_image)
    st.markdown('## Grayscale Image of the Driving License')
    st.image(gray_image, caption='GrayScale Image of the Driving License')
    extracted_data = get_card_data(gray_image)
    license_validity, valid_date = get_card_validity(extracted_data)
    st.markdown('## Information from the Driving License')
    st.info('The Driving License Validity is **{}/{}/{}**'.format(valid_date.day, valid_date.month, valid_date.year))
    st.info('**{}**'.format(license_validity))
