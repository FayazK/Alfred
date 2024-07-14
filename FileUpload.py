import streamlit as st
import os
from io import StringIO
from server import File_Upload

os.makedirs('./data', exist_ok=True)

def file_upload():
    st.markdown("<h1 style='text-align: center;'>Upload file</h1>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Choose and Upload file", type = ['csv','xlsx'], accept_multiple_files=False,label_visibility="hidden")

    if uploaded_files is not None:
        save_path = os.path.join('./data', uploaded_files.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_files.getbuffer())
        response = File_Upload(file_name=uploaded_files)
        if response['code'] == '200':
            st.success(f"Assistant created and now live for chating")
        elif response['code'] == '404':
            st.error('There is some eror araise while creating assistant')

# file_upload()