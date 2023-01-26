import streamlit as st
import glob
from PIL import Image
from io import BytesIO

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
    image_files = glob.glob("CardValidityChecker/Images/Credit Card*") + glob.glob("CardValidityChecker/Images/Driving License*")
    return image_files


image_files = load_images()
n_rows = int(1 + len(image_files) // 2)
rows = [st.columns(3) for _ in range(n_rows)]
cols = [column for row in rows for column in row]

for col, file in zip(cols, image_files):
    parts = file.split("/")
    file_name = parts[-1].split(".")[0]
    image = Image.open(file)
    image = image.resize((700, 500))
    col.image(image)
    buf = BytesIO()
    image.save(buf, format="png")
    byte_im = buf.getvalue()
    btn = col.download_button(
        label="Download {}".format(file_name),
        data=byte_im,
        file_name=file,
        mime="image/png",
    )
