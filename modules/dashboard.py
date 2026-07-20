import pandas as pd
import streamlit as st
from .core import read_table, metric_money

def show_dashboard():
    st.title("📊 Executive Dashboard")
    students, fees, staff, attendance = [read_table(x) for x in ["students","fees","staff","attendance"]]
    paid=pd.to_numeric(fees.get("amount_paid",pd.Series(dtype=float)),errors="coerce").fillna(0).sum()
    due=pd.to_numeric(fees.get("amount_due",pd.Series(dtype=float)),errors="coerce").fillna(0).sum()
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Students",len(students)); c2.metric("Active Staff",len(staff)); c3.metric("Fees Collected",metric_money(paid)); c4.metric("Outstanding",metric_money(max(due-paid,0)))
    st.divider()
    a,b=st.columns(2)
    with a:
        st.subheader("Enrollment by Curriculum")
        if len(students): st.bar_chart(students["curriculum"].value_counts())
        else: st.info("Register students to see enrollment analytics.")
    with b:
        st.subheader("Attendance Summary")
        if len(attendance): st.bar_chart(attendance["status"].value_counts())
        else: st.info("Record attendance to see trends.")
    st.subheader("Quick Actions")
    st.info("Use the menu to register students, receive fees, record grades, manage staff, send messages, track transport, clinic, library, payroll, construction, and inventory.")
