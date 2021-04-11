# pip install openpyxl
import pandas as pd
import streamlit as st
import zipfile
import base64
import os

# Web App Title
st.markdown('''
# **Auto Excel File Combining Machine**
- upload a zip file containing multiples files and 'VOILA!'
---
''')

# Excel file merge function
def excel_file_merge(zip_file_name):
    df = pd.DataFrame()
    archive = zipfile.ZipFile(zip_file_name, 'r')
    with zipfile.ZipFile(zip_file_name, "r") as f:
        for file in f.namelist():
          xlfile = archive.open(file)
          if file.endswith('.xlsx'):
            df_xl = pd.read_excel(xlfile, engine='openpyxl')
            df_xl['Note'] = file
            # Appends content of each Excel file iteratively
            df = df.append(df_xl, ignore_index=True)
    return df


# Upload data files via zip
with st.sidebar.header('1. Upload  ZIP file'):
    uploaded_file = st.sidebar.file_uploader("excel-containing ZIP file", type=["zip"])


# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_file.csv">Download Merged File as CSV</a>'
    return href

def xldownload(df):
    df.to_excel('data.xlsx', index=False)
    data = open('data.xlsx', 'rb').read()
    b64 = base64.b64encode(data).decode('UTF-8')
    #b64 = base64.b64encode(xl.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/xls;base64,{b64}" download="merged_file.xlsx">Download Merged File as XLSX</a>'
    return href

# Main panel
if st.sidebar.button('Submit'):
    #@st.cache
    df = excel_file_merge(uploaded_file)
    st.header('**Combined data**')
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)
    st.markdown(xldownload(df), unsafe_allow_html=True)
else:
    st.info('Please Upload .zip file')