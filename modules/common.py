from pathlib import Path
import pandas as pd

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

def load_table(name: str) -> pd.DataFrame:
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
    return pd.DataFrame(columns=config["columns"])

def save_table(name: str, df: pd.DataFrame) -> None:
    df.to_csv(TABLES[name]["file"], index=False)

def delete_row(name: str, df: pd.DataFrame, index: int) -> pd.DataFrame:
    updated = df.drop(index=index).reset_index(drop=True)
    save_table(name, updated)
    return updated
