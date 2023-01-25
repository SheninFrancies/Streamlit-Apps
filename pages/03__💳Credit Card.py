import streamlit as st
import io
import numpy as np
from PIL import Image
import cv2
import pandas as pd
import pytesseract
from pytesseract import Output
import arrow
import dateutil

st.set_page_config(layout='wide', page_title='Credit Card')

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
uploaded_file = st.sidebar.file_uploader('Upload an Image of the Credit Card',  type=['jpg', 'png'])

# Title and Intro
if uploaded_file is None:
    st.title('Credit Card Validity Checker')
    st.text('Explore this page to check the validity of the Credit Card.')


# Convert Image
def save_image(byteImage):
    bytesImg = io.BytesIO(byteImage)
    imgFile = Image.open(bytesImg)
    return imgFile


## Preprocess the Image
def image_preprocessing(image, resize_width=900, resize_height=600):
    resize_image = cv2.resize(image, (resize_width, resize_height))
    gray = cv2.cvtColor(resize_image, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(resize_image, 50, 250)

    # Create a rectangular Kernel and a Square Kernel
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    # TOPHAT Morphing
    tophat = cv2.morphologyEx(img_canny, cv2.MORPH_TOPHAT, rectKernel)
    # Threshold
    thresh = cv2.threshold(tophat, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

    img_final = cv2.bitwise_and(gray, thresh)

    return img_final, gray


## Get the Expiry and Check Validity
def credit_card_validity(image_preprocessed, confidence=30):
    data = pytesseract.image_to_data(image_preprocessed, output_type=Output.DICT)
    extract = []
    for i in range(len(data['text'])):
        if data['conf'][i] > confidence:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            extract.append(data['text'][i])
    # Convert to Series
    SeriesData = pd.Series(extract)
    extracted_data = SeriesData[SeriesData.str.contains('^\d{2}\/\d{2}$')]
    expiry = extracted_data.to_list()
    dates = []
    for date in expiry:
        date = arrow.get(date, 'MM/YY').date()
        dates.append(date)
    valid_date = max(dates)
    validity_date = str(valid_date.month) + '/' + str(valid_date.year)
    current_date = arrow.utcnow().date()
    if current_date > valid_date:
        validity_period = dateutil.relativedelta.relativedelta(current_date, valid_date)
        validity_duration = 'Credit Card is INVALID and is {} years, {} months and {} days past the validity.'.format(
            validity_period.years, validity_period.months, validity_period.days)

    else:
        validity_period = dateutil.relativedelta.relativedelta(valid_date, current_date)
        validity_duration = 'Credit Card is VALID and can be used for {} years, {} months and {} days.'.format(
            validity_period.years, validity_period.months, validity_period.days)
    return validity_date, validity_duration


# Check if the file has been uploaded
if uploaded_file is not None:
    file = uploaded_file.read()
    path = save_image(file)
    st.title('Credit Card Validity Checker')
    st.markdown('## Original Credit Card')
    st.image(path, width=500, caption='Original Credit Card')
    file_bytes = np.asarray(bytearray(file), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    image_preprocessed, gray_image = image_preprocessing(opencv_image)
    st.markdown('## Grayscale Image of the Credit Card')
    st.image(gray_image, caption='GrayScale Image of the Credit Card')
    st.markdown('## Preprocessed Image of the Credit Card')
    st.image(image_preprocessed, caption='Preprocessed Image of the Credit Card')
    validity_date, validity_duration = credit_card_validity(image_preprocessed, gray_image)
    st.markdown('## Information from the Credit Card')
    st.info('The Credit Card Validity (MM/YYYY) is **{}.**'.format(validity_date))
    st.info('**{}**'.format(validity_duration))
    