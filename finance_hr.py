import streamlit as st
from .core import data_editor

def show_operations():
    st.title("🏫 School Operations")
    tabs=st.tabs(["Library","Transport","Clinic","Boarding","Kitchen & Meals"])
    items=[("library","Library Register"),("transport","Transport Routes & Vehicles"),("clinic","Clinic Records"),("boarding","Boarding & Dormitories"),("meals","Kitchen & Meal Plans")]
    for tab,(name,title) in zip(tabs,items):
        with tab: data_editor(name,title)
