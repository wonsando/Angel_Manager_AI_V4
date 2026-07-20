import datetime as dt, uuid
import pandas as pd
import streamlit as st
from .core import append_row, data_editor, read_table, metric_money

def show_fees():
    st.title("💰 Fees, Receipts & Balances")
    t1,t2,t3=st.tabs(["Receive Payment","Ledger","Statements"])
    with t1:
        students=read_table("students")
        with st.form("fee_form",clear_on_submit=True):
            a,b,c=st.columns(3)
            adm=a.text_input("Admission Number")
            name=b.text_input("Student Name")
            fee_type=c.selectbox("Fee Type",["Tuition","Transport","Meals","Boarding","Activities","Uniform","Other"])
            due=a.number_input("Amount Due",min_value=0.0)
            paid=b.number_input("Amount Paid",min_value=0.0)
            method=c.selectbox("Payment Method",["M-Pesa","Cash","Bank","Card","Cheque","Other"])
            ref=a.text_input("Payment Reference")
            receiver=b.text_input("Received By",value=st.session_state.get("username","admin"))
            date=c.date_input("Date",dt.date.today())
            ok=st.form_submit_button("Save Payment & Generate Receipt",use_container_width=True)
        if ok:
            receipt=f"R-{dt.datetime.now():%Y%m%d}-{str(uuid.uuid4())[:6].upper()}"
            append_row("fees",dict(receipt_no=receipt,date=date,admission_no=adm,student_name=name,fee_type=fee_type,amount_due=due,amount_paid=paid,payment_method=method,reference=ref,balance=max(due-paid,0),received_by=receiver))
            st.success(f"Payment saved. Receipt: {receipt}")
            receipt_text = f"""ANGEL MEMORIAL ADVENTIST INTERNATIONAL ACADEMY
Receipt: {receipt}
Student: {name}
Admission: {adm}
Amount Paid: KES {paid:,.2f}
Method: {method}
Reference: {ref}
Date: {date}
"""
            st.download_button("Download Receipt", receipt_text, file_name=f"{receipt}.txt")
    with t2: data_editor("fees","Fee Ledger")
    with t3:
        df=read_table("fees")
        adm=st.text_input("Admission number for statement")
        if adm and len(df):
            out=df[df["admission_no"].astype(str).str.lower()==adm.lower()]
            st.dataframe(out,use_container_width=True)
            paid=pd.to_numeric(out["amount_paid"],errors="coerce").fillna(0).sum(); due=pd.to_numeric(out["amount_due"],errors="coerce").fillna(0).sum()
            st.metric("Statement Balance",metric_money(max(due-paid,0)))
