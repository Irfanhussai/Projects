import streamlit as st
# from backend.auth import login_user
# from backend.auth import login_user
# from ..backend.auth import login_user
import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.auth import login_user

def show():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        token = login_user(username, password)
        if token:
            st.session_state["token"] = token
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")
