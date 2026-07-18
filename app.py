import io, zipfile
import streamlit as st
from core import DATA

def show_settings():
    st.title("⚙️ System Settings")
    t1,t2,t3=st.tabs(["School Profile","Backup & Export","Cloud Readiness"])
    with t1:
        st.text_input("School Name",value="Angel Memorial Adventist International Academy")
        st.text_input("Country",value="Kenya")
        st.text_input("Currency",value="KES")
        st.selectbox("Academic Year",[2026,2027,2028,2029])
        st.button("Save Profile")
    with t2:
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED) as z:
            for p in DATA.glob("*.csv"): z.write(p,p.name)
        st.download_button("Download Complete Data Backup",buf.getvalue(),file_name="Angel_Manager_AI_Backup.zip",use_container_width=True)
    with t3:
        st.success("The app is deployment-ready and works immediately with local CSV storage.")
        st.info("Supabase cloud synchronization, file uploads, live SMS/WhatsApp, M-Pesa, and multi-factor authentication require external service credentials. These can be connected later without rebuilding the interface.")
        secret_example = chr(10).join(['SUPABASE_URL = "..."','SUPABASE_KEY = "..."','ADMIN_USERNAME = "admin"','ADMIN_PASSWORD_HASH = "..."'])
        st.code(secret_example, language="toml")
