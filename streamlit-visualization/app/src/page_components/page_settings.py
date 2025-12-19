import streamlit as st

from core.logger import get_logger

logger = get_logger("page_settings")

def page_settings():
    with st.container(border=True):
        st.text("There are settings.")
        logger.info("Settings page loaded successfully")