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
st.text('Users can download TEST IMAGES of the respective card(s) from this section of the application.')
st.text('The downloaded Image(s) can then be used to check its validity.')
st.info('The application does not currently support downloading all the test images together.')

st.subheader('Credit Card')
st.text('In this section, users can check the Validity of the uploaded Credit Card.')
st.text('Given an image of the Credit Card, users can know whether the card is valid or not.')
st.warning('Discretion: Images of low resolution and/or large dimensions may not work as intended.')

st.subheader('Driving License')
st.text('In this section, users can check the Validity of the uploaded Driving License.')
st.text('Given an image of the Credit Card, users can know whether the License is valid or not and for how long.')
st.warning('Discretion: Images of low resolution and/or large dimensions may not work as intended.')
