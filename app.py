import streamlit as st
from pathlib import Path
import hashlib

from modules.dashboard import show_dashboard
from modules.students import show_students
from modules.fees import show_fees
from modules.attendance import show_attendance
from modules.staff import show_staff
from modules.construction import show_construction
from modules.inventory import show_inventory
from modules.ai_assistant import show_ai_assistant
from modules.common import using_cloud_database

st.set_page_config(
    page_title="Angel Manager AI",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA = Path("data")
DATA.mkdir(exist_ok=True)

try:
    DEFAULT_USERNAME = str(st.secrets.get("APP_USERNAME", "admin"))
    default_password = str(st.secrets.get("APP_PASSWORD", "angel123"))
except Exception:
    DEFAULT_USERNAME = "admin"
    default_password = "angel123"
DEFAULT_PASSWORD_HASH = hashlib.sha256(default_password.encode()).hexdigest()

def password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def login_screen():
    st.title("🏫 Angel Manager AI")
    st.subheader("Angel Memorial Adventist International Academy")
    st.info("Sign in to access the management system.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

    if submitted:
        if username == DEFAULT_USERNAME and password_hash(password) == DEFAULT_PASSWORD_HASH:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Incorrect username or password.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_screen()
    st.stop()

st.sidebar.title("🏫 Angel Manager AI")
st.sidebar.caption("Professional Edition — Version 4")
st.sidebar.write(f"Signed in as **{st.session_state.get('username', 'admin')}**")
st.sidebar.caption("☁️ Supabase online database" if using_cloud_database() else "💾 Local storage mode")

section = st.sidebar.radio(
    "Choose a module",
    [
        "Dashboard",
        "Students",
        "Fees",
        "Attendance",
        "Staff",
        "Construction",
        "Inventory",
        "AI Assistant",
    ],
)

if st.sidebar.button("Log Out", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()

if section == "Dashboard":
    show_dashboard()
elif section == "Students":
    show_students()
elif section == "Fees":
    show_fees()
elif section == "Attendance":
    show_attendance()
elif section == "Staff":
    show_staff()
elif section == "Construction":
    show_construction()
elif section == "Inventory":
    show_inventory()
elif section == "AI Assistant":
    show_ai_assistant()
