import streamlit as st

import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.auth import verify_token

def show():
    st.title("🏠 Dashboard")
    token = st.session_state.get("token")
    
    if token:
        user_data = verify_token(token)
        if user_data:
            st.write(f"Welcome, {user_data['username']} ({user_data['role']})")
        else:
            st.error("Session expired. Please login again.")
    else:
        st.error("Please login first.")
