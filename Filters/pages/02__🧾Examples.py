import streamlit as st
import glob
from PIL import Image
from io import BytesIO
from scipy.interpolate import UnivariateSpline

st.set_page_config(layout='wide', page_title='Examples')

# Title and Intro
st.title('Example Files')
st.text('Here are some example cards to download and play around with.')


# Remove Footer and Menu
hide_footer = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility:hidden;}
    </style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)


def load_images():
    image_files = glob.glob("Filters/Images/Image*")
    return image_files

images = load_images()
n_rows = int(1 + len(images) // 2)
rows = [st.columns(3) for _ in range(n_rows)]
cols = [column for row in rows for column in row]

for col, file in zip(cols, images):
    parts = file.split("/")
    file_name = parts[-1].split(".")[0].split("-")[1]
    image = Image.open(file)
    image_display = image.resize((600, 420))
    col.image(image_display)
    buf = BytesIO()
    image.save(buf, format="png")
    byte_im = buf.getvalue()
    btn = col.download_button(
        label=f"Download {file_name}.png",
        data=byte_im,
        file_name=file,
        mime="image/png",
    )