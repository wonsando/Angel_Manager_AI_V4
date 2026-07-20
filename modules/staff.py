import datetime as dt
import streamlit as st
from .core import append_row, data_editor

def show_staff():
    st.title("👩‍🏫 Staff & Human Resources")
    t1,t2=st.tabs(["Add Staff","Staff Directory"])
    with t1:
        with st.form("staff",clear_on_submit=True):
            a,b,c=st.columns(3)
            sid=a.text_input("Staff ID"); name=b.text_input("Full Name"); role=c.text_input("Role")
            dept=a.text_input("Department"); phone=b.text_input("Phone"); email=c.text_input("Email")
            et=a.selectbox("Employment Type",["Permanent","Contract","Part-time","Volunteer"]); sal=b.number_input("Monthly Salary",min_value=0.0); start=c.date_input("Start Date",dt.date.today())
            status=a.selectbox("Status",["Active","On Leave","Suspended","Exited"])
            ok=st.form_submit_button("Save Staff Member",use_container_width=True)
        if ok: append_row("staff",dict(staff_id=sid,name=name,role=role,department=dept,phone=phone,email=email,employment_type=et,salary=sal,start_date=start,status=status)); st.success("Staff member saved.")
    with t2: data_editor("staff","Staff Directory")
