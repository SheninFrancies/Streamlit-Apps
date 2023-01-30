import cv2
import streamlit as st
import io
import numpy as np
from PIL import Image
from scipy.interpolate import UnivariateSpline

st.set_page_config(layout='wide', page_title='Filters for Images')

# Remove Footer and Menu
hide_footer = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility:hidden;}
    </style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)


## Pencil Sketch
@st.cache
def PencilSketch(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (21, 21), 0, 0)
    final_image = cv2.divide(gray_image, blurred_image, scale=256)
    ret, mask = cv2.threshold(final_image, 70, 255, cv2.THRESH_BINARY)
    sketched_image = cv2.bitwise_and(mask, final_image)
    return sketched_image


## Warm and Cool Filter
def LUT_8UC1(x, y):
    spl = UnivariateSpline(x, y)
    return spl(range(256))


increase_pixel = LUT_8UC1([0, 64, 128, 192, 256], [0, 70, 140, 210, 256])
decrease_pixel = LUT_8UC1([0, 64, 128, 192, 256], [0, 30, 80, 120, 192])


@st.cache
def warming_effect(image):
    red, green, blue = cv2.split(image)
    red = cv2.LUT(red, increase_pixel).astype(np.uint8)
    blue = cv2.LUT(blue, decrease_pixel).astype(np.uint8)
    rgb_image = cv2.merge((red, green, blue))
    hue, saturation, value = cv2.split(cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV))
    saturation = cv2.LUT(saturation, increase_pixel).astype(np.uint8)
    final_image = cv2.cvtColor(cv2.merge((hue, saturation, value)), cv2.COLOR_HSV2RGB)
    return final_image


@st.cache
def cooling_effect(image):
    red, green, blue = cv2.split(image)
    red = cv2.LUT(red, decrease_pixel).astype(np.uint8)
    blue = cv2.LUT(blue, increase_pixel).astype(np.uint8)
    rgb_image = cv2.merge((red, green, blue))
    hue, saturation, value = cv2.split(cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV))
    saturation = cv2.LUT(saturation, decrease_pixel).astype(np.uint8)
    final_image = cv2.cvtColor(cv2.merge((hue, saturation, value)), cv2.COLOR_HSV2RGB)
    return final_image


## Cartoon Effect
@st.cache
def color_quantization(image, k):
    data = np.float32(image).reshape((-1,3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    success, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(image.shape)
    return result


@st.cache
def cartoon_effect(image):
    quantized_image = color_quantization(image, 7)
    bilateral_image = cv2.bilateralFilter(quantized_image, 8, 150, 150)
    gray_image = cv2.cvtColor(bilateral_image, cv2.COLOR_BGR2GRAY)
    edge_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9,9)
    cartoon_image = cv2.bitwise_and(bilateral_image, bilateral_image, mask=edge_image)
    return cartoon_image


# Sidebar Setup
st.sidebar.title('Select a File')
uploaded_file = st.sidebar.file_uploader('Upload an Image of the Credit Card', type=['jpg', 'png'])

# Title and Intro
if uploaded_file is None:
    st.title('Filters for Images')
    st.text('Upload an Image to get started.')

option = st.sidebar.selectbox('Select the Filter', ('Pencil Sketch', 'Warm Effect', 'Cool Effect', 'Cartoon Effect'))


# # Convert Image
# def save_image(byteImage):
#     bytesImg = io.BytesIO(byteImage)
#     imgFile = Image.open(bytesImg)
#     return imgFile

buffer = io.BytesIO()

# Check if the file has been uploaded
if uploaded_file is not None:
    file = uploaded_file.read()
    filename = uploaded_file.name.split('.')[0]
    st.title(option)
    col1, col2 = st.columns(2)
    col1.image(uploaded_file, caption="Uploaded Image")
    file_bytes = np.asarray(bytearray(file), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    if option == 'Pencil Sketch':
        sketch = PencilSketch(opencv_image)
        col2.image(sketch, caption='Pencil Sketch')
        im = Image.fromarray(sketch)
        im.save(buffer, format="PNG")
        col1, col2, col3, col4, col5 = st.columns(5)
        btn = col3.download_button(
            label= f"Download **{filename}.png**",
            data=buffer,
            file_name=f"{filename}.png",
            mime="image/png",
        )
    if option == 'Warm Effect':
        warm_image = warming_effect(opencv_image)
        col2.image(warm_image, caption='Warm Effect')
        im = Image.fromarray(warm_image)
        im.save(buffer, format="PNG")
        col1, col2, col3, col4, col5 = st.columns(5)
        btn = col3.download_button(
            label=f"Download **{filename}.png**",
            data=buffer,
            file_name=f"{filename}.png",
            mime="image/png",
        )
    if option == 'Cool Effect':
        cool_image = cooling_effect(opencv_image)
        col2.image(cool_image, caption='Cool Effect')
        im = Image.fromarray(cool_image)
        im.save(buffer, format="PNG")
        col1, col2, col3, col4, col5 = st.columns(5)
        btn = col3.download_button(
            label=f"Download **{filename}.png**",
            data=buffer,
            file_name=f"{filename}.png",
            mime="image/png",
        )
    if option == 'Cartoon Effect':
        cartoon_image = cartoon_effect(opencv_image)
        col2.image(cartoon_image, caption='Cartoon Effect')
        im = Image.fromarray(cartoon_image)
        im.save(buffer, format="PNG")
        col1, col2, col3, col4, col5 = st.columns(5)
        btn = col3.download_button(
            label=f"Download **{filename}.png**",
            data=buffer,
            file_name=f"{filename}.png",
            mime="image/png",
        )
