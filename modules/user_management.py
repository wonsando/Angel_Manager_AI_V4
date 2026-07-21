import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timezone
from typing import Any

import streamlit as st


USERS_FILE = "data/users.json"
PBKDF2_ITERATIONS = 310_000

ROLE_PERMISSIONS = {
    "Director": [
        "Dashboard",
        "Students & Admissions",
        "Fees & Receipts",
        "Attendance",
        "Academics & Reports",
        "Staff & HR",
        "Operations",
        "Finance & Payroll",
        "Communication & Portals",
        "Construction",
        "Inventory & Procurement",
        "AI Assistant",
        "System Settings",
        "User Management",
    ],
    "Headteacher": [
        "Dashboard",
        "Students & Admissions",
        "Attendance",
        "Academics & Reports",
        "Staff & HR",
        "Communication & Portals",
    ],
    "Bursar": [
        "Dashboard",
        "Fees & Receipts",
        "Finance & Payroll",
        "Inventory & Procurement",
    ],
    "Teacher": [
        "Dashboard",
        "Students & Admissions",
        "Attendance",
        "Academics & Reports",
        "Communication & Portals",
    ],
    "Receptionist": [
        "Dashboard",
        "Students & Admissions",
        "Attendance",
        "Communication & Portals",
    ],
    "Construction Manager": [
        "Dashboard",
        "Construction",
        "Inventory & Procurement",
        "Operations",
    ],
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_storage() -> None:
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    if not os.path.exists(USERS_FILE):
        save_users([])


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations_text, salt_hex, digest_hex = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False

        calculated = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations_text),
        )
        return hmac.compare_digest(calculated.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def load_users() -> list[dict[str, Any]]:
    _ensure_storage()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_users(users: list[dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    temp_file = f"{USERS_FILE}.tmp"
    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)
    os.replace(temp_file, USERS_FILE)


def authenticate_user(username: str, password: str) -> dict[str, Any] | None:
    clean_username = username.strip().lower()
    for user in load_users():
        if (
            user.get("username", "").lower() == clean_username
            and user.get("active", True)
            and verify_password(password, user.get("password_hash", ""))
        ):
            return user
    return None


def get_permissions(role: str) -> list[str]:
    return ROLE_PERMISSIONS.get(role, [])


def user_can_access(user: dict[str, Any] | None, module_name: str) -> bool:
    if not user:
        return False
    return module_name in get_permissions(str(user.get("role", "")))


def render() -> None:
    st.header("👥 User Management")
    st.caption("Create separate accounts and control what each worker can access.")

    users = load_users()
    create_tab, accounts_tab, roles_tab = st.tabs(
        ["Create Account", "Manage Accounts", "Roles & Permissions"]
    )

    with create_tab:
        with st.form("create_user_form", clear_on_submit=True):
            full_name = st.text_input("Worker's full name")
            username = st.text_input("Username")
            password = st.text_input("Temporary password", type="password")
            confirm_password = st.text_input("Confirm temporary password", type="password")
            role = st.selectbox("Role", list(ROLE_PERMISSIONS))
            active = st.checkbox("Account active", value=True)
            submitted = st.form_submit_button("Create Account")

        if submitted:
            clean_username = username.strip().lower()
            if not full_name.strip():
                st.error("Enter the worker's full name.")
            elif len(clean_username) < 3:
                st.error("Username must contain at least 3 characters.")
            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")
            elif password != confirm_password:
                st.error("The passwords do not match.")
            elif any(
                user.get("username", "").lower() == clean_username for user in users
            ):
                st.error("That username already exists.")
            else:
                users.append(
                    {
                        "username": clean_username,
                        "full_name": full_name.strip(),
                        "password_hash": hash_password(password),
                        "role": role,
                        "active": active,
                        "must_change_password": True,
                        "created_at": _utc_now(),
                        "updated_at": _utc_now(),
                    }
                )
                save_users(users)
                st.success(f"Account created for {full_name.strip()} as {role}.")
                st.rerun()

    with accounts_tab:
        if not users:
            st.info("No worker accounts have been created yet.")
        else:
            for index, user in enumerate(users):
                status = "Active" if user.get("active", True) else "Disabled"
                label = (
                    f"{user.get('full_name', 'Unknown')} — "
                    f"{user.get('role', 'Unknown')} — {status}"
                )

                with st.expander(label):
                    st.write(f"**Username:** {user.get('username', '')}")
                    st.write(f"**Role:** {user.get('role', '')}")
                    st.write(f"**Status:** {status}")

                    role_names = list(ROLE_PERMISSIONS)
                    current_role = user.get("role", "Teacher")
                    role_index = (
                        role_names.index(current_role)
                        if current_role in role_names
                        else 0
                    )

                    new_role = st.selectbox(
                        "Change role",
                        role_names,
                        index=role_index,
                        key=f"role_{index}",
                    )
                    new_status = st.checkbox(
                        "Account active",
                        value=user.get("active", True),
                        key=f"active_{index}",
                    )
                    new_password = st.text_input(
                        "New temporary password",
                        type="password",
                        key=f"password_{index}",
                        help="Leave blank to keep the current password.",
                    )

                    if st.button(
                        "Save Changes",
                        key=f"save_{index}",
                        use_container_width=True,
                    ):
                        if new_password and len(new_password) < 8:
                            st.error("The new password must contain at least 8 characters.")
                        else:
                            users[index]["role"] = new_role
                            users[index]["active"] = new_status
                            users[index]["updated_at"] = _utc_now()

                            if new_password:
                                users[index]["password_hash"] = hash_password(new_password)
                                users[index]["must_change_password"] = True

                            save_users(users)
                            st.success("Account updated.")
                            st.rerun()

    with roles_tab:
        for role_name, permissions in ROLE_PERMISSIONS.items():
            with st.expander(role_name):
                for permission in permissions:
                    st.write(f"✅ {permission}")
