import streamlit as st
import pymongo
import gridfs

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["skb_db"]
fs = gridfs.GridFS(db)

st.title("📂 View & Download Files")

# Fetch file list
files = [file.filename for file in fs.find()]

if not files:
    st.info("No files available.")
else:
    selected_file = st.selectbox("Select a file to download:", files)

    if st.button("Download"):
        file_data = fs.find_one({"filename": selected_file})
        if file_data:
            st.download_button(
                label="📥 Download File",
                data=file_data.read(),
                file_name=selected_file,
                mime="application/octet-stream"
            )
        else:
            st.error("File not found.")
