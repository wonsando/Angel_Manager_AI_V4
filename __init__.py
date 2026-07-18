from pathlib import Path
import hashlib, json
import pandas as pd
import streamlit as st

DATA = Path("data")
DEFAULT_USER = "admin"
DEFAULT_PASSWORD = "angel123"

TABLES = {
 "students": ["admission_no","student_name","dob","gender","curriculum","class_program","guardian_name","phone","email","medical_notes","transport_route","status"],
 "fees": ["receipt_no","date","admission_no","student_name","fee_type","amount_due","amount_paid","payment_method","reference","balance","received_by"],
 "attendance": ["date","person_type","person_id","name","class_department","status","time_in","notes"],
 "staff": ["staff_id","name","role","department","phone","email","employment_type","salary","start_date","status"],
 "grades": ["term","year","admission_no","student_name","curriculum","class_program","subject","score","grade","teacher","remarks"],
 "timetable": ["day","start_time","end_time","class_program","subject","teacher","room"],
 "library": ["item_id","title","category","borrower_id","borrower_name","date_out","due_date","status"],
 "transport": ["route_id","route_name","vehicle","driver","phone","capacity","students","status"],
 "clinic": ["date","student_id","student_name","complaint","action","medicine","guardian_contacted","staff"],
 "boarding": ["student_id","student_name","dormitory","bed_no","house_parent","status"],
 "meals": ["date","meal","menu","estimated_servings","actual_servings","cost","notes"],
 "payroll": ["month","staff_id","staff_name","basic_salary","allowances","deductions","net_pay","status"],
 "expenses": ["date","category","description","supplier","amount","payment_method","reference","approved_by"],
 "messages": ["date","audience","channel","subject","message","status"],
 "construction": ["project_id","project_name","contractor","start_date","target_date","budget","spent","progress","status","notes"],
 "inventory": ["item_code","item_name","category","quantity","unit","reorder_level","unit_cost","supplier","location","status"],
 "users": ["username","full_name","role","email","status"]
}

def init_data():
    DATA.mkdir(exist_ok=True)
    for name, cols in TABLES.items():
        p=DATA/f"{name}.csv"
        if not p.exists(): pd.DataFrame(columns=cols).to_csv(p,index=False)
    if "logged_in" not in st.session_state: st.session_state.logged_in=False

def read_table(name):
    p=DATA/f"{name}.csv"
    try: return pd.read_csv(p)
    except Exception: return pd.DataFrame(columns=TABLES[name])

def write_table(name, df):
    df.to_csv(DATA/f"{name}.csv", index=False)

def append_row(name, row):
    df=read_table(name)
    df=pd.concat([df,pd.DataFrame([row])],ignore_index=True)
    write_table(name,df)

def metric_money(v):
    try: return f"KES {float(v):,.0f}"
    except: return "KES 0"

def password_hash(s): return hashlib.sha256(s.encode()).hexdigest()

def login_screen():
    st.title("🏫 Angel Manager AI Enterprise")
    st.subheader("Angel Memorial Adventist International Academy")
    st.caption("One integrated platform for school management")
    with st.form("login"):
        u=st.text_input("Username")
        p=st.text_input("Password",type="password")
        ok=st.form_submit_button("Sign In",use_container_width=True)
    if ok:
        expected_user=st.secrets.get("ADMIN_USERNAME",DEFAULT_USER)
        expected_hash=st.secrets.get("ADMIN_PASSWORD_HASH",password_hash(DEFAULT_PASSWORD))
        if u==expected_user and password_hash(p)==expected_hash:
            st.session_state.logged_in=True; st.session_state.username=u; st.session_state.role="Administrator"; st.rerun()
        else: st.error("Incorrect username or password.")

def sidebar_header():
    st.sidebar.title("🏫 Angel Manager AI")
    st.sidebar.caption("Enterprise Edition — Version 6")
    st.sidebar.success("Online app ready")
    st.sidebar.write(f"Signed in as **{st.session_state.get('username','admin')}**")
    if st.sidebar.button("Log Out",use_container_width=True):
        st.session_state.logged_in=False; st.rerun()

def data_editor(name, title, height=360):
    st.subheader(title)
    df=read_table(name)
    edited=st.data_editor(df, num_rows="dynamic", use_container_width=True, height=height, key=f"ed_{name}")
    if st.button(f"Save {title}", key=f"save_{name}"):
        write_table(name,edited); st.success("Saved successfully.")
