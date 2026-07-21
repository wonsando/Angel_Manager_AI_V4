from pathlib import Path
import hashlib

import pandas as pd
import streamlit as st

from modules.user_management import authenticate_user


DATA = Path("data")
DEFAULT_USER = "admin"
DEFAULT_PASSWORD = "angel123"

TABLES = {
    "students": ["admission_no", "student_name", "dob", "gender", "curriculum", "class_program", "guardian_name", "phone", "email", "medical_notes", "transport_route", "status"],
    "fees": ["receipt_no", "date", "admission_no", "student_name", "fee_type", "amount_due", "amount_paid", "payment_method", "reference", "balance", "received_by"],
    "attendance": ["date", "person_type", "person_id", "name", "class_department", "status", "time_in", "notes"],
    "staff": ["staff_id", "name", "role", "department", "phone", "email", "employment_type", "salary", "start_date", "status"],
    "grades": ["term", "year", "admission_no", "student_name", "curriculum", "class_program", "subject", "score", "grade", "teacher", "remarks"],
    "timetable": ["day", "start_time", "end_time", "class_program", "subject", "teacher", "room"],
    "library": ["item_id", "title", "category", "borrower_id", "borrower_name", "date_out", "due_date", "status"],
    "transport": ["route_id", "route_name", "vehicle", "driver", "phone", "capacity", "students", "status"],
    "clinic": ["date", "student_id", "student_name", "complaint", "action", "medicine", "guardian_contacted", "staff"],
    "boarding": ["student_id", "student_name", "dormitory", "bed_no", "house_parent", "status"],
    "meals": ["date", "meal", "menu", "estimated_servings", "actual_servings", "cost", "notes"],
    "payroll": ["month", "staff_id", "staff_name", "basic_salary", "allowances", "deductions", "net_pay", "status"],
    "expenses": ["date", "category", "description", "supplier", "amount", "payment_method", "reference", "approved_by"],
    "messages": ["date", "audience", "channel", "subject", "message", "status"],
    "construction": ["project_id", "project_name", "contractor", "start_date", "target_date", "budget", "spent", "progress", "status", "notes"],
    "inventory": ["item_code", "item_name", "category", "quantity", "unit", "reorder_level", "unit_cost", "supplier", "location", "status"],
    "users": ["username", "full_name", "role", "email", "status"],
}


def init_data():
    DATA.mkdir(exist_ok=True)

    for name, columns in TABLES.items():
        path = DATA / f"{name}.csv"
        if not path.exists():
            pd.DataFrame(columns=columns).to_csv(path, index=False)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


def read_table(name):
    path = DATA / f"{name}.csv"
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=TABLES[name])


def write_table(name, dataframe):
    dataframe.to_csv(DATA / f"{name}.csv", index=False)


def append_row(name, row):
    dataframe = read_table(name)
    dataframe = pd.concat(
        [dataframe, pd.DataFrame([row])],
        ignore_index=True,
    )
    write_table(name, dataframe)


def metric_money(value):
    try:
        return f"KES {float(value):,.0f}"
    except (TypeError, ValueError):
        return "KES 0"


def password_hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def login_screen():
    st.title("🏫 Angel Manager AI Enterprise")
    st.subheader("Angel Memorial Adventist International Academy")
    st.caption("One integrated platform for school management")

    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True,
        )

    if submitted:
        expected_user = st.secrets.get("ADMIN_USERNAME", DEFAULT_USER)
        expected_hash = st.secrets.get(
            "ADMIN_PASSWORD_HASH",
            password_hash(DEFAULT_PASSWORD),
        )

        if (
            username.strip() == expected_user
            and password_hash(password) == expected_hash
        ):
            st.session_state.logged_in = True
            st.session_state.username = expected_user
            st.session_state.full_name = "School Director"
            st.session_state.role = "Director"
            st.rerun()

        worker = authenticate_user(username, password)

        if worker:
            st.session_state.logged_in = True
            st.session_state.username = worker["username"]
            st.session_state.full_name = worker.get(
                "full_name",
                worker["username"],
            )
            st.session_state.role = worker.get("role", "Teacher")
            st.rerun()

        st.error("Incorrect username or password.")


def sidebar_header():
    st.sidebar.title("🏫 Angel Manager AI")
    st.sidebar.caption("Enterprise Edition — Version 6")
    st.sidebar.success("Online app ready")

    full_name = st.session_state.get(
        "full_name",
        st.session_state.get("username", "admin"),
    )
    role = st.session_state.get("role", "Director")

    st.sidebar.write(f"Signed in as **{full_name}**")
    st.sidebar.caption(f"Role: {role}")

    if st.sidebar.button("Log Out", use_container_width=True):
        for key in [
            "logged_in",
            "username",
            "full_name",
            "role",
        ]:
            st.session_state.pop(key, None)
        st.rerun()


def data_editor(name, title, height=360):
    st.subheader(title)
    dataframe = read_table(name)

    edited = st.data_editor(
        dataframe,
        num_rows="dynamic",
        use_container_width=True,
        height=height,
        key=f"ed_{name}",
    )

    if st.button(f"Save {title}", key=f"save_{name}"):
        write_table(name, edited)
        st.success("Saved successfully.")
