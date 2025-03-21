import streamlit as st
import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.search import search_documents

def show():
    st.title("🔎 Search Documents")
    query = st.text_input("Search")
    file_type = st.selectbox("File Type", ["All", "PDF", "DOCX", "TXT"])
    
    if st.button("Search"):
        results = search_documents(query, file_type, None, None)
        for doc in results:
            st.write(f"📄 **{doc['filename']}** - {doc['upload_date']}")
