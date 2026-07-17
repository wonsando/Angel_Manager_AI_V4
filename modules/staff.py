import streamlit as st
import pandas as pd
from modules.common import load_table, save_table

def show_staff():
    st.title("👨‍🏫 Staff Management")
    df = load_table("staff")

    with st.form("staff_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        staff_id = c1.text_input("Staff ID")
        name = c2.text_input("Staff Name")
        role = c1.text_input("Role")
        phone = c2.text_input("Phone Number")
        email = c1.text_input("Email")
        salary = c2.number_input("Monthly Salary", min_value=0.0)
        status = st.selectbox("Employment Status", ["Active", "On Leave", "Suspended", "Former"])
        submitted = st.form_submit_button("Save Staff", use_container_width=True)

    if submitted:
        if not staff_id.strip() or not name.strip():
            st.error("Staff ID and name are required.")
        else:
            new = pd.DataFrame([[staff_id, name, role, phone, email, salary, status]], columns=df.columns)
            df = pd.concat([df, new], ignore_index=True)
            save_table("staff", df)
            st.success("Staff member saved.")
            st.rerun()

    st.dataframe(df, use_container_width=True)
