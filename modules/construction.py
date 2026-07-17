import streamlit as st
import pandas as pd
from datetime import date
from modules.common import load_table, save_table

def show_construction():
    st.title("🏗️ Construction Management")
    df = load_table("construction")

    with st.form("construction_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        d = c1.date_input("Date", date.today())
        project = c2.text_input("Project Name")
        contractor = c1.text_input("Contractor/Supplier")
        budget = c2.number_input("Budget", min_value=0.0)
        spent = c1.number_input("Amount Spent", min_value=0.0)
        status = c2.selectbox("Status", ["Planned", "In Progress", "Paused", "Complete"])
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save Project Update", use_container_width=True)

    if submitted:
        new = pd.DataFrame([[d, project, contractor, budget, spent, status, notes]], columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        save_table("construction", df)
        st.success("Construction record saved.")
        st.rerun()

    budget_total = pd.to_numeric(df["Budget"], errors="coerce").fillna(0).sum()
    spent_total = pd.to_numeric(df["Amount Spent"], errors="coerce").fillna(0).sum()
    remaining = budget_total - spent_total

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Budget", f"KES {budget_total:,.0f}")
    c2.metric("Total Spent", f"KES {spent_total:,.0f}")
    c3.metric("Remaining", f"KES {remaining:,.0f}")

    st.dataframe(df, use_container_width=True)
