import datetime as dt
import streamlit as st
from .core import append_row, data_editor

def show_communication():
    st.title("📱 Communication & Portals")
    t1,t2,t3=st.tabs(["Compose Message","Message Log","User Accounts"])
    with t1:
        with st.form("msg",clear_on_submit=True):
            audience=st.selectbox("Audience",["All Parents","Selected Class","Staff","Students","Board","Individual"])
            channel=st.multiselect("Channels",["SMS","WhatsApp","Email","Portal Notice"])
            subject=st.text_input("Subject"); message=st.text_area("Message",height=180)
            ok=st.form_submit_button("Queue Message",use_container_width=True)
        if ok: append_row("messages",dict(date=dt.datetime.now(),audience=audience,channel=", ".join(channel),subject=subject,message=message,status="Queued")); st.success("Message queued. Connect an SMS/WhatsApp provider later to send automatically.")
    with t2: data_editor("messages","Message Log")
    with t3: data_editor("users","Portal Users")
