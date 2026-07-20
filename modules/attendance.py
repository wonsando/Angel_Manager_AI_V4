import datetime as dt
import streamlit as st
from .core import append_row, data_editor

def show_attendance():
    st.title("📝 Attendance")
    t1,t2=st.tabs(["Record Attendance","Attendance Register"])
    with t1:
        with st.form("att",clear_on_submit=True):
            a,b,c=st.columns(3)
            date=a.date_input("Date",dt.date.today()); typ=b.selectbox("Person Type",["Student","Staff"]); pid=c.text_input("ID / Admission Number")
            name=a.text_input("Name"); group=b.text_input("Class / Department"); status=c.selectbox("Status",["Present","Absent","Late","Excused","Sick"])
            time=a.time_input("Time In"); notes=b.text_input("Notes")
            ok=st.form_submit_button("Record Attendance",use_container_width=True)
        if ok: append_row("attendance",dict(date=date,person_type=typ,person_id=pid,name=name,class_department=group,status=status,time_in=time,notes=notes)); st.success("Attendance recorded.")
    with t2: data_editor("attendance","Attendance Register")
