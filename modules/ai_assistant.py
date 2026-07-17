import streamlit as st
import pandas as pd
from modules.common import load_table

def show_ai_assistant():
    st.title("🤖 Angel AI Assistant")
    st.caption("Ask questions about the information saved in your system.")

    question = st.text_area("Ask a management question")
    if st.button("Get Guidance", use_container_width=True) and question.strip():
        q = question.lower()

        students = load_table("students")
        fees = load_table("fees")
        staff = load_table("staff")
        construction = load_table("construction")
        inventory = load_table("inventory")

        if "how many student" in q or "number of student" in q:
            st.success(f"There are {len(students)} registered students.")
        elif "how many staff" in q or "number of staff" in q:
            st.success(f"There are {len(staff)} registered staff members.")
        elif "fees collected" in q or "money collected" in q:
            total = pd.to_numeric(fees["Amount Paid"], errors="coerce").fillna(0).sum()
            st.success(f"Total recorded fees collected: KES {total:,.0f}.")
        elif "balance" in q:
            total = pd.to_numeric(fees["Balance"], errors="coerce").fillna(0).sum()
            st.success(f"Total recorded fee balances: KES {total:,.0f}.")
        elif "construction" in q or "building" in q:
            budget = pd.to_numeric(construction["Budget"], errors="coerce").fillna(0).sum()
            spent = pd.to_numeric(construction["Amount Spent"], errors="coerce").fillna(0).sum()
            st.write(f"Construction budget: KES {budget:,.0f}")
            st.write(f"Construction spending: KES {spent:,.0f}")
            st.write(f"Remaining: KES {budget - spent:,.0f}")
        elif "low stock" in q or "restock" in q:
            if inventory.empty:
                st.info("No inventory has been recorded.")
            else:
                qty = pd.to_numeric(inventory["Quantity"], errors="coerce").fillna(0)
                minimum = pd.to_numeric(inventory["Minimum Stock"], errors="coerce").fillna(0)
                low = inventory[qty <= minimum]
                if low.empty:
                    st.success("No items currently need restocking.")
                else:
                    st.dataframe(low, use_container_width=True)
        else:
            st.info(
                "Try asking: How many students are registered? "
                "How much fees have been collected? "
                "What is the construction balance? "
                "Which inventory items need restocking?"
            )
