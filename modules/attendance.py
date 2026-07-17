import streamlit as st
import pandas as pd
from datetime import date
from modules.common import load_table, save_table

def show_attendance():
    st.title("✅ Attendance")
    df = load_table("attendance")
    students = load_table("students")
    names = [""] + students["Student Name"].dropna().astype(str).tolist()

    with st.form("attendance_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        d = c1.date_input("Date", date.today())
        admission = c2.text_input("Admission Number")
        name = c1.selectbox("Student Name", names)
        status = c2.selectbox("Status", ["Present", "Absent", "Late", "Excused"])
        notes = st.text_input("Notes")
        submitted = st.form_submit_button("Save Attendance", use_container_width=True)

    if submitted:
        new = pd.DataFrame([[d, admission, name, status, notes]], columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        save_table("attendance", df)
        st.success("Attendance saved.")
        st.rerun()

    st.dataframe(df, use_container_width=True)
