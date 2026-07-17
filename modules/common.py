from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

DATA = Path("data")
DATA.mkdir(exist_ok=True)

TABLES = {
    "students": {
        "file": DATA / "students.csv",
        "columns": [
            "Admission No", "Student Name", "Date of Birth", "Gender",
            "Curriculum", "Class", "Parent Name", "Phone", "Parent Email",
            "Emergency Contact", "Transport Route"
        ],
    },
    "fees": {
        "file": DATA / "fees.csv",
        "columns": ["Date", "Admission No", "Student Name", "Amount Paid", "Term", "Balance", "Payment Method"],
    },
    "attendance": {
        "file": DATA / "attendance.csv",
        "columns": ["Date", "Admission No", "Student Name", "Status", "Notes"],
    },
    "staff": {
        "file": DATA / "staff.csv",
        "columns": ["Staff ID", "Staff Name", "Role", "Phone", "Email", "Salary", "Employment Status"],
    },
    "construction": {
        "file": DATA / "construction.csv",
        "columns": ["Date", "Project", "Contractor", "Budget", "Amount Spent", "Status", "Notes"],
    },
    "inventory": {
        "file": DATA / "inventory.csv",
        "columns": ["Item", "Category", "Quantity", "Unit Cost", "Total Value", "Location", "Minimum Stock"],
    },
}

# Supabase-safe database column names.
DB_COLUMNS = {
    "students": {
        "Admission No": "admission_no", "Student Name": "student_name", "Date of Birth": "date_of_birth",
        "Gender": "gender", "Curriculum": "curriculum", "Class": "class_name", "Parent Name": "parent_name",
        "Phone": "phone", "Parent Email": "parent_email", "Emergency Contact": "emergency_contact",
        "Transport Route": "transport_route",
    },
    "fees": {
        "Date": "payment_date", "Admission No": "admission_no", "Student Name": "student_name",
        "Amount Paid": "amount_paid", "Term": "term", "Balance": "balance", "Payment Method": "payment_method",
    },
    "attendance": {
        "Date": "attendance_date", "Admission No": "admission_no", "Student Name": "student_name",
        "Status": "status", "Notes": "notes",
    },
    "staff": {
        "Staff ID": "staff_id", "Staff Name": "staff_name", "Role": "role", "Phone": "phone",
        "Email": "email", "Salary": "salary", "Employment Status": "employment_status",
    },
    "construction": {
        "Date": "record_date", "Project": "project", "Contractor": "contractor", "Budget": "budget",
        "Amount Spent": "amount_spent", "Status": "status", "Notes": "notes",
    },
    "inventory": {
        "Item": "item", "Category": "category", "Quantity": "quantity", "Unit Cost": "unit_cost",
        "Total Value": "total_value", "Location": "location", "Minimum Stock": "minimum_stock",
    },
}


def _secret(name: str) -> str:
    try:
        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""


@st.cache_resource(show_spinner=False)
def get_supabase_client():
    url = _secret("SUPABASE_URL")
    key = _secret("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None


def using_cloud_database() -> bool:
    return get_supabase_client() is not None


def _empty(name: str) -> pd.DataFrame:
    return pd.DataFrame(columns=TABLES[name]["columns"])


def _db_to_display(name: str, rows: list[dict[str, Any]]) -> pd.DataFrame:
    reverse = {db: display for display, db in DB_COLUMNS[name].items()}
    cleaned = []
    for row in rows:
        cleaned.append({reverse[k]: v for k, v in row.items() if k in reverse})
    df = pd.DataFrame(cleaned)
    for col in TABLES[name]["columns"]:
        if col not in df.columns:
            df[col] = ""
    return df[TABLES[name]["columns"]]


def _display_to_db(name: str, df: pd.DataFrame) -> list[dict[str, Any]]:
    rename = DB_COLUMNS[name]
    records = df.rename(columns=rename).to_dict(orient="records")
    cleaned: list[dict[str, Any]] = []
    for record in records:
        row: dict[str, Any] = {}
        for key, value in record.items():
            if pd.isna(value):
                row[key] = None
            elif hasattr(value, "isoformat"):
                row[key] = value.isoformat()
            else:
                row[key] = value.item() if hasattr(value, "item") else value
        cleaned.append(row)
    return cleaned


def load_table(name: str) -> pd.DataFrame:
    client = get_supabase_client()
    if client is not None:
        try:
            response = client.table(name).select("*").order("created_at").execute()
            return _db_to_display(name, response.data or [])
        except Exception as exc:
            st.warning(f"Cloud database could not be read. Using local backup. Details: {exc}")

    config = TABLES[name]
    path = config["file"]
    if path.exists():
        try:
            df = pd.read_csv(path)
            for column in config["columns"]:
                if column not in df.columns:
                    df[column] = ""
            return df[config["columns"]]
        except Exception:
            pass
    return _empty(name)


def save_table(name: str, df: pd.DataFrame) -> None:
    client = get_supabase_client()
    if client is not None:
        records = _display_to_db(name, df)
        try:
            # Simple and dependable for the current small school dataset:
            # replace the table's rows with the latest DataFrame.
            client.table(name).delete().neq("id", 0).execute()
            if records:
                client.table(name).insert(records).execute()
            return
        except Exception as exc:
            st.error(f"Cloud save failed: {exc}")
            raise

    df.to_csv(TABLES[name]["file"], index=False)


def delete_row(name: str, df: pd.DataFrame, index: int) -> pd.DataFrame:
    updated = df.drop(index=index).reset_index(drop=True)
    save_table(name, updated)
    return updated
