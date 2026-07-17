import streamlit as st
import pandas as pd
from modules.common import load_table, save_table

def show_inventory():
    st.title("📦 Inventory Management")
    df = load_table("inventory")

    with st.form("inventory_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        item = c1.text_input("Item")
        category = c2.text_input("Category")
        quantity = c1.number_input("Quantity", min_value=0.0)
        unit_cost = c2.number_input("Unit Cost", min_value=0.0)
        location = c1.text_input("Location")
        minimum = c2.number_input("Minimum Stock Level", min_value=0.0)
        submitted = st.form_submit_button("Save Item", use_container_width=True)

    if submitted:
        total = quantity * unit_cost
        new = pd.DataFrame(
            [[item, category, quantity, unit_cost, total, location, minimum]],
            columns=df.columns,
        )
        df = pd.concat([df, new], ignore_index=True)
        save_table("inventory", df)
        st.success("Inventory item saved.")
        st.rerun()

    if not df.empty:
        qty = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
        minimum = pd.to_numeric(df["Minimum Stock"], errors="coerce").fillna(0)
        low = df[qty <= minimum]
        if not low.empty:
            st.warning("The following items need restocking:")
            st.dataframe(low, use_container_width=True)

    st.dataframe(df, use_container_width=True)
