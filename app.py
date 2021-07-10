import predictor
import dashboard
import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state='auto')

PAGES = {
    "Country Classification Predictor": predictor,
    "Country Development Dashboard": dashboard
    }

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()