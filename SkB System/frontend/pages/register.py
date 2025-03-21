import streamlit as st
import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.auth import register_user

def show():
    st.title("📝 Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Viewer", "Contributor", "Admin"])

    if st.button("Register"):
        message = register_user(username, password, role)
        st.success(message)
