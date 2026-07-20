import datetime as dt
import streamlit as st
from .core import append_row, data_editor, read_table

def show_students():
    st.title("👨‍🎓 Students & Admissions")
    t1,t2,t3=st.tabs(["Register Student","Student Directory","Documents & Profiles"])
    with t1:
        with st.form("student_form",clear_on_submit=True):
            a,b,c=st.columns(3)
            adm=a.text_input("Admission Number")
            name=b.text_input("Student Name")
            dob=c.date_input("Date of Birth",value=dt.date(2015,1,1))
            gender=a.selectbox("Gender",["Female","Male","Other"])
            curriculum=b.selectbox("Curriculum",["CBC","British / IGCSE","American","International Baccalaureate","Special Education","Daycare / Early Years"])
            program=c.text_input("Class / Program")
            guardian=a.text_input("Parent / Guardian")
            phone=b.text_input("Phone Number")
            email=c.text_input("Email")
            medical=a.text_area("Medical / Allergy Notes")
            route=b.text_input("Transport Route")
            status=c.selectbox("Status",["Active","Applicant","Suspended","Alumni"])
            ok=st.form_submit_button("Save Student",use_container_width=True)
        if ok:
            if not adm or not name: st.error("Admission number and student name are required.")
            else:
                append_row("students",dict(admission_no=adm,student_name=name,dob=dob,gender=gender,curriculum=curriculum,class_program=program,guardian_name=guardian,phone=phone,email=email,medical_notes=medical,transport_route=route,status=status)); st.success("Student saved.")
    with t2: data_editor("students","Student Directory")
    with t3:
        st.subheader("Student Profile Search")
        df=read_table("students")
        q=st.text_input("Search by name or admission number")
        if q and len(df): st.dataframe(df[df.astype(str).apply(lambda r:r.str.contains(q,case=False).any(),axis=1)],use_container_width=True)
        st.caption("Document upload can be connected to Supabase Storage later; core records are already integrated here.")
