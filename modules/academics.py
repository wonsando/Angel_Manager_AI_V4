import streamlit as st
from .core import append_row, data_editor

def grade(score):
    try:
        s=float(score)
        return "A" if s>=80 else "B" if s>=70 else "C" if s>=60 else "D" if s>=50 else "E"
    except: return ""

def show_academics():
    st.title("📚 Academics, Exams & Reports")
    t1,t2,t3=st.tabs(["Enter Grades","Gradebook","Timetable"])
    with t1:
        with st.form("grade",clear_on_submit=True):
            a,b,c=st.columns(3)
            term=a.selectbox("Term",["Term 1","Term 2","Term 3","Semester 1","Semester 2"]); year=b.number_input("Year",2020,2100,2026); adm=c.text_input("Admission Number")
            name=a.text_input("Student Name"); curr=b.selectbox("Curriculum",["CBC","British / IGCSE","American","International Baccalaureate","Special Education"]); cls=c.text_input("Class / Program")
            subject=a.text_input("Subject"); score=b.number_input("Score",0.0,100.0); teacher=c.text_input("Teacher"); remarks=a.text_input("Remarks")
            ok=st.form_submit_button("Save Grade",use_container_width=True)
        if ok: append_row("grades",dict(term=term,year=year,admission_no=adm,student_name=name,curriculum=curr,class_program=cls,subject=subject,score=score,grade=grade(score),teacher=teacher,remarks=remarks)); st.success("Grade saved.")
    with t2: data_editor("grades","Gradebook")
    with t3: data_editor("timetable","Master Timetable")
