import json
from pathlib import Path
from abc import ABC, abstractmethod

import streamlit as st

# ----------------------------------------------------------------------
# Database
# ----------------------------------------------------------------------

DATABASE = "school_data.json"


def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
    return {"students": [], "teachers": []}


def save(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


# ----------------------------------------------------------------------
# Domain classes (same structure as the original script, minus input())
# ----------------------------------------------------------------------

class Person(ABC):
    @abstractmethod
    def set_roles(self):
        pass

    @abstractmethod
    def register(self, **kwargs):
        pass

    @abstractmethod
    def show_details(self, identifier):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email


class Student(Person):
    def set_roles(self):
        return "student"

    def register(self, name, age, email, roll_no):
        if not Person.validate_email(email):
            return False, "Invalid email address."

        for i in data["students"]:
            if i["roll_no"] == roll_no:
                return False, f"A student with roll_no '{roll_no}' is already registered."

        data["students"].append({
            "name": name,
            "age": age,
            "email": email,
            "roll_no": roll_no,
            "grades": {},
        })
        save(data)
        return True, f"Student {name} has registered."

    def find(self, roll_no):
        for i in data["students"]:
            if i["roll_no"] == roll_no:
                return i
        return None

    def show_details(self, roll_no):
        record = self.find(roll_no)
        if not record:
            return None
        avg = sum(record["grades"].values()) / len(record["grades"]) if record["grades"] else 0
        return record, avg

    def add_grade(self, roll_no, subject, marks):
        record = self.find(roll_no)
        if not record:
            return False, "Student not found."
        record["grades"][subject] = marks
        save(data)
        return True, "Grade added successfully."


class Teacher(Person):
    def set_roles(self):
        return "teacher"

    def register(self, name, age, email, subject, emp_id):
        if not Person.validate_email(email):
            return False, "Invalid email address."

        for i in data["teachers"]:
            if i["emp_id"] == emp_id:
                return False, f"A teacher with emp_id '{emp_id}' is already registered."

        data["teachers"].append({
            "name": name,
            "age": age,
            "email": email,
            "subject": subject,
            "emp_id": emp_id,
        })
        save(data)
        return True, f"Teacher {name} has registered."

    def find(self, emp_id):
        for i in data["teachers"]:
            if i["emp_id"] == emp_id:
                return i
        return None

    def show_details(self, emp_id):
        return self.find(emp_id)


stud = Student()
teacher = Teacher()

# ----------------------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------------------

st.set_page_config(page_title="School Management System", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0f1117; }
    div[data-testid="stMetric"] {
        background-color: #1a1d29;
        border: 1px solid #2a2e3f;
        border-radius: 10px;
        padding: 14px 18px;
    }
    .block-container { padding-top: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎓 School Management System")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "Register Student",
            "Register Teacher",
            "Add Grade",
            "View Student Details",
            "View Teacher Details",
        ],
        label_visibility="collapsed",
    )

# ---------------- Dashboard ----------------
if page == "Dashboard":
    col1, col2 = st.columns(2)
    col1.metric("Total Students", len(data["students"]))
    col2.metric("Total Teachers", len(data["teachers"]))

    st.subheader("Students")
    if data["students"]:
        st.dataframe(
            [
                {
                    "Name": s["name"],
                    "Roll No": s["roll_no"],
                    "Age": s["age"],
                    "Email": s["email"],
                    "Subjects Graded": len(s["grades"]),
                    "Average": round(sum(s["grades"].values()) / len(s["grades"]), 2) if s["grades"] else "—",
                }
                for s in data["students"]
            ],
            use_container_width=True,
        )
    else:
        st.info("No students registered yet.")

    st.subheader("Teachers")
    if data["teachers"]:
        st.dataframe(
            [
                {
                    "Name": t["name"],
                    "Emp ID": t["emp_id"],
                    "Age": t["age"],
                    "Email": t["email"],
                    "Subject": t["subject"],
                }
                for t in data["teachers"]
            ],
            use_container_width=True,
        )
    else:
        st.info("No teachers registered yet.")

# ---------------- Register Student ----------------
elif page == "Register Student":
    st.subheader("Register a New Student")
    with st.form("register_student_form", clear_on_submit=True):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        email = st.text_input("Email")
        roll_no = st.text_input("Roll No")
        submitted = st.form_submit_button("Register")

    if submitted:
        if not name or not roll_no or not email:
            st.error("Please fill in all fields.")
        else:
            ok, msg = stud.register(name, int(age), email, roll_no)
            (st.success if ok else st.error)(msg)

# ---------------- Register Teacher ----------------
elif page == "Register Teacher":
    st.subheader("Register a New Teacher")
    with st.form("register_teacher_form", clear_on_submit=True):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        emp_id = st.text_input("Employee ID")
        submitted = st.form_submit_button("Register")

    if submitted:
        if not name or not emp_id or not email or not subject:
            st.error("Please fill in all fields.")
        else:
            ok, msg = teacher.register(name, int(age), email, subject, emp_id)
            (st.success if ok else st.error)(msg)

# ---------------- Add Grade ----------------
elif page == "Add Grade":
    st.subheader("Add a Grade")
    if not data["students"]:
        st.info("No students registered yet. Register a student first.")
    else:
        with st.form("add_grade_form", clear_on_submit=True):
            roll_no = st.text_input("Roll No")
            subject = st.text_input("Subject")
            marks = st.number_input("Marks", min_value=0, max_value=100, step=1)
            submitted = st.form_submit_button("Add Grade")

        if submitted:
            if not roll_no or not subject:
                st.error("Please fill in all fields.")
            else:
                ok, msg = stud.add_grade(roll_no, subject, int(marks))
                (st.success if ok else st.error)(msg)

# ---------------- View Student Details ----------------
elif page == "View Student Details":
    st.subheader("Student Details")
    roll_no = st.text_input("Enter Roll No")
    if st.button("Search") and roll_no:
        result = stud.show_details(roll_no)
        if result is None:
            st.error("Student not found.")
        else:
            record, avg = result
            c1, c2 = st.columns(2)
            c1.write(f"**Name:** {record['name']}")
            c1.write(f"**Age:** {record['age']}")
            c2.write(f"**Email:** {record['email']}")
            c2.write(f"**Roll No:** {record['roll_no']}")

            st.write("**Grades:**")
            if record["grades"]:
                st.table(
                    [{"Subject": k, "Marks": v} for k, v in record["grades"].items()]
                )
            else:
                st.write("No grades recorded yet.")
            st.metric("Average", round(avg, 2))

# ---------------- View Teacher Details ----------------
elif page == "View Teacher Details":
    st.subheader("Teacher Details")
    emp_id = st.text_input("Enter Employee ID")
    if st.button("Search") and emp_id:
        record = teacher.show_details(emp_id)
        if record is None:
            st.error("Teacher not found.")
        else:
            c1, c2 = st.columns(2)
            c1.write(f"**Name:** {record['name']}")
            c1.write(f"**Age:** {record['age']}")
            c2.write(f"**Email:** {record['email']}")
            c2.write(f"**Subject:** {record['subject']}")
            c2.write(f"**Emp ID:** {record['emp_id']}")