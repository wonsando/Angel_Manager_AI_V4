import streamlit as st
import pandas as pd
from datetime import date
from modules.common import load_table, save_table

def show_fees():
    st.title("💰 Fees Management")
    df = load_table("fees")
    students = load_table("students")

    names = [""] + students["Student Name"].dropna().astype(str).tolist()

    with st.form("fees_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        d = c1.date_input("Payment Date", date.today())
        admission = c2.text_input("Admission Number")
        name = c1.selectbox("Student Name", names)
        amount = c2.number_input("Amount Paid", min_value=0.0)
        term = c1.selectbox("Term", ["Term 1", "Term 2", "Term 3"])
        balance = c2.number_input("Remaining Balance", min_value=0.0)
        method = st.selectbox("Payment Method", ["M-Pesa", "Bank", "Cash", "Cheque", "Other"])
        submitted = st.form_submit_button("Record Payment", use_container_width=True)

    if submitted:
        if not admission.strip() or not name.strip():
            st.error("Admission number and student name are required.")
        else:
            new = pd.DataFrame([[d, admission, name, amount, term, balance, method]], columns=df.columns)
            df = pd.concat([df, new], ignore_index=True)
            save_table("fees", df)
            st.success("Payment recorded.")
            st.rerun()

    paid = pd.to_numeric(df["Amount Paid"], errors="coerce").fillna(0).sum()
    balances = pd.to_numeric(df["Balance"], errors="coerce").fillna(0).sum()
    c1, c2 = st.columns(2)
    c1.metric("Total Collected", f"KES {paid:,.0f}")
    c2.metric("Recorded Balances", f"KES {balances:,.0f}")

    st.dataframe(df, use_container_width=True)
    st.download_button("Download Fees Report", df.to_csv(index=False), "fees_report.csv", "text/csv")
