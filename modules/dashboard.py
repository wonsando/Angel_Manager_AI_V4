import streamlit as st
import pandas as pd
from modules.common import load_table

def show_dashboard():
    st.title("📊 Executive Dashboard")

    students = load_table("students")
    fees = load_table("fees")
    staff = load_table("staff")
    construction = load_table("construction")
    inventory = load_table("inventory")

    total_fees = pd.to_numeric(fees.get("Amount Paid"), errors="coerce").fillna(0).sum()
    total_balances = pd.to_numeric(fees.get("Balance"), errors="coerce").fillna(0).sum()
    total_budget = pd.to_numeric(construction.get("Budget"), errors="coerce").fillna(0).sum()
    total_spent = pd.to_numeric(construction.get("Amount Spent"), errors="coerce").fillna(0).sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", len(students))
    c2.metric("Staff", len(staff))
    c3.metric("Fees Collected", f"KES {total_fees:,.0f}")
    c4.metric("Outstanding Balances", f"KES {total_balances:,.0f}")

    c5, c6, c7 = st.columns(3)
    c5.metric("Construction Budget", f"KES {total_budget:,.0f}")
    c6.metric("Construction Spent", f"KES {total_spent:,.0f}")
    c7.metric("Inventory Items", len(inventory))

    st.subheader("Management Alerts")
    if total_spent > total_budget and total_budget > 0:
        st.error("Construction spending is above the recorded budget.")
    else:
        st.success("Construction spending is currently within the recorded budget.")

    low_stock = inventory.copy()
    if not low_stock.empty:
        qty = pd.to_numeric(low_stock["Quantity"], errors="coerce").fillna(0)
        minimum = pd.to_numeric(low_stock["Minimum Stock"], errors="coerce").fillna(0)
        low_stock = low_stock[qty <= minimum]

    if not low_stock.empty:
        st.warning(f"{len(low_stock)} inventory item(s) need restocking.")
        st.dataframe(low_stock, use_container_width=True)
    else:
        st.info("No low-stock alerts.")

    st.subheader("Recent Student Registrations")
    st.dataframe(students.tail(5), use_container_width=True)
