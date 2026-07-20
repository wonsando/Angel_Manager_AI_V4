import streamlit as st
from .core import data_editor, read_table

def show_inventory():
    st.title("📦 Inventory & Procurement")
    data_editor("inventory","Inventory Register")
    df=read_table("inventory")
    if len(df):
        try:
            low=df[df["quantity"].astype(float)<=df["reorder_level"].astype(float)]
            if len(low): st.warning(f"{len(low)} item(s) need reordering."); st.dataframe(low,use_container_width=True)
        except: pass
