import streamlit as st
import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.document_management import upload_document
from backend.auth import verify_token

def show():
    st.title("📤 Upload Document")
    token = st.session_state.get("token")

    if token:
        user_data = verify_token(token)
        if user_data and user_data["role"] in ["Admin", "Contributor"]:
            uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
            tags = st.text_input("Enter tags (comma-separated)")
            
            if uploaded_file and st.button("Upload"):
                upload_document(uploaded_file, user_data["username"], tags)
                st.success("File uploaded successfully!")
        else:
            st.warning("You do not have permission to upload documents.")
    else:
        st.error("Please login first.")
