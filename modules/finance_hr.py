import streamlit as st
from .core import data_editor

def show_finance_hr():
    st.title("💼 Finance, Payroll & Budgeting")
    t1,t2=st.tabs(["Payroll","Expenses & Budget"])
    with t1: data_editor("payroll","Payroll Register")
    with t2: data_editor("expenses","Expense Register")
