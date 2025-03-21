

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from frontend.pages import login, register, dashboard, upload, search, viewer  # Import viewer

# Page Selection
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Register", "Dashboard", "Upload", "Search", "viewer"])

# Page Routing
if page == "Login":
    login.show()
elif page == "Register":
    register.show()
elif page == "Dashboard":
    dashboard.show()
elif page == "Upload":
    upload.show()
elif page == "Search":
    search.show()
elif page == "viewer":  # Add viewer.py
    viewer.show()
