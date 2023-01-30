import streamlit as st

st.set_page_config(layout='wide', page_title='About')

# Remove Footer and Menu
hide_footer = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility:hidden;}
    </style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

# Title and Intro
st.title('Navigating the Application')

st.subheader('Examples')
st.text('Users can download TEST IMAGES here for use in Filters.')
st.info('The application does not currently support downloading all the test images together.')

st.subheader('Filters')
st.text('Users can upload an image in this section and select the filters from the select box.')
st.markdown('#### Pencil Sketch')
st.text('This Filter provides the Pencil Sketch of the Image.')

st.markdown('#### Warm and Cool Effects')
st.text('The Filters can be selected separately and provides the temperature-aspect - Warm or Cool Effect - of the Image.')

st.markdown('#### Cartoon Effect')
st.text('The Filters provides a cartoonized effect of the Image.')

st.title('Acknowledgements')
st.info('The source code of this application is based on the concepts from the book "OpenCV: Computer Vision Projects with Python".')
st.info('Special thanks to [Aditi Rastogi](https://github.com/AditiRastogi250701) for her contributions towards the Cartoon Effect.')