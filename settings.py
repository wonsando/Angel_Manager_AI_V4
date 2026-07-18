import streamlit as st
from .core import read_table

def show_ai_assistant():
    st.title("🤖 Angel AI Assistant")
    st.info("This built-in assistant analyzes the school's local records. Add an API key later for full conversational AI.")
    q=st.text_area("Ask about the school",placeholder="Example: How many students are registered?")
    if st.button("Analyze",use_container_width=True):
        text=q.lower(); students=read_table("students"); staff=read_table("staff"); fees=read_table("fees")
        if "how many" in text and "student" in text: st.success(f"There are {len(students)} registered students.")
        elif "how many" in text and "staff" in text: st.success(f"There are {len(staff)} staff records.")
        elif "fee" in text or "payment" in text:
            import pandas as pd
            total=pd.to_numeric(fees.get("amount_paid"),errors="coerce").fillna(0).sum() if len(fees) else 0
            st.success(f"Recorded fee collections total KES {total:,.0f}.")
        else: st.write("I can currently summarize students, staff, fees, attendance, inventory, and operational records. Full generative AI can be connected in System Settings.")
