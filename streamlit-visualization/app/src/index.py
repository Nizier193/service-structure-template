import streamlit as st

from src.page_components import page_settings
from src.page_components import ping_test

def index():
    tab1, tab2, tab3 = st.tabs(["Main", "Ping", "Settings"])

    with tab1:
        st.text("Main")  
        st.text("Основная страничка.")

    with tab2:
        ping_test.page_ping()

    with tab3:
        page_settings.page_settings()