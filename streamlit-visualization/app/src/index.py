import streamlit as st

from src.page_components import page_settings

def index():
    tab1, tab2 = st.tabs(["Index", "Settings"])

    with tab1:
        st.text("Index")        

    with tab2:
        page_settings.page_settings()