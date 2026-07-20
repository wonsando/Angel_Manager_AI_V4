import streamlit as st
from .core import data_editor

def show_construction():
    st.title("🏗️ Construction & Maintenance")
    data_editor("construction","Construction Projects")
