import hashlib
from pathlib import Path
import streamlit as st

from modules.core import init_data, login_screen, sidebar_header
from modules.dashboard import show_dashboard
from modules.students import show_students
from modules.fees import show_fees
from modules.attendance import show_attendance
from modules.staff import show_staff
from modules.academics import show_academics
from modules.operations import show_operations
from modules.finance_hr import show_finance_hr
from modules.communication import show_communication
from modules.construction import show_construction
from modules.inventory import show_inventory
from modules.ai_assistant import show_ai_assistant
from modules.settings import show_settings

st.set_page_config(page_title="Angel Manager AI Enterprise", page_icon="🏫", layout="wide", initial_sidebar_state="expanded")
init_data()

if not st.session_state.get("logged_in", False):
    login_screen()
    st.stop()

sidebar_header()
section = st.sidebar.radio("Choose a module", [
    "Dashboard", "Students & Admissions", "Fees & Receipts", "Attendance",
    "Academics & Reports", "Staff & HR", "Operations", "Finance & Payroll",
    "Communication & Portals", "Construction", "Inventory & Procurement",
    "AI Assistant", "System Settings"
])

routes = {
    "Dashboard": show_dashboard,
    "Students & Admissions": show_students,
    "Fees & Receipts": show_fees,
    "Attendance": show_attendance,
    "Academics & Reports": show_academics,
    "Staff & HR": show_staff,
    "Operations": show_operations,
    "Finance & Payroll": show_finance_hr,
    "Communication & Portals": show_communication,
    "Construction": show_construction,
    "Inventory & Procurement": show_inventory,
    "AI Assistant": show_ai_assistant,
    "System Settings": show_settings,
}
routes[section]()
