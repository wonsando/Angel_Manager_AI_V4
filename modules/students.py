import streamlit as st
import pandas as pd
from datetime import date
from modules.common import load_table, save_table

CURRICULA = [
    "CBC",
    "Special Education",
    "International Baccalaureate (IB)",
    "British Curriculum",
    "American Curriculum",
]

CLASSES = [
    "CBC - Creche", "CBC - Playgroup", "CBC - PP1", "CBC - PP2",
    "CBC - Grade 1", "CBC - Grade 2", "CBC - Grade 3", "CBC - Grade 4",
    "CBC - Grade 5", "CBC - Grade 6", "CBC - Grade 7", "CBC - Grade 8",
    "CBC - Grade 9", "CBC - Senior School",
    "Special Education - Early Intervention", "Special Education - Autism Support",
    "Special Education - Learning Disabilities", "Special Education - Hearing Impairment",
    "Special Education - Visual Impairment", "Special Education - Physical Disabilities",
    "Special Education - Gifted and Talented",
    "IB - Primary Years Programme (PYP)", "IB - Middle Years Programme (MYP)",
    "IB - Diploma Programme (DP)", "IB - Career-related Programme (CP)",
    "British - Early Years Foundation Stage (EYFS)", "British - Key Stage 1",
    "British - Key Stage 2", "British - Key Stage 3", "British - IGCSE",
    "British - AS Level", "British - A Level",
    "American - Elementary School", "American - Middle School",
    "American - High School", "American - Advanced Placement (AP)",
    "American - Common Core",
]

def show_students():
    st.title("👩‍🎓 Student Management")
    df = load_table("students")

    with st.expander("Register a New Student", expanded=True):
        with st.form("student_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            admission = c1.text_input("Admission Number")
            name = c2.text_input("Student Name")
            dob = c1.date_input("Date of Birth", date(2018, 1, 1))
            gender = c2.selectbox("Gender", ["Female", "Male", "Other"])
            curriculum = c1.selectbox("Curriculum", CURRICULA)
            class_name = c2.selectbox("Class / Program", CLASSES)
            parent = c1.text_input("Parent/Guardian Name")
            phone = c2.text_input("Phone Number")
            email = c1.text_input("Parent Email")
            emergency = c2.text_input("Emergency Contact")
            route = st.text_input("Transport Route")
            submitted = st.form_submit_button("Save Student", use_container_width=True)

        if submitted:
            if not admission.strip() or not name.strip():
                st.error("Admission number and student name are required.")
            elif admission in df["Admission No"].astype(str).values:
                st.error("That admission number already exists.")
            else:
                new = pd.DataFrame([[
                    admission, name, dob, gender, curriculum, class_name,
                    parent, phone, email, emergency, route
                ]], columns=df.columns)
                df = pd.concat([df, new], ignore_index=True)
                save_table("students", df)
                st.success("Student registered successfully.")
                st.rerun()

    search = st.text_input("Search students")
    shown = df
    if search.strip():
        mask = df.astype(str).apply(
            lambda row: row.str.contains(search, case=False, na=False).any(), axis=1
        )
        shown = df[mask]

    st.dataframe(shown, use_container_width=True)
    st.download_button(
        "Download Student List",
        data=shown.to_csv(index=False),
        file_name="students.csv",
        mime="text/csv",
    )
