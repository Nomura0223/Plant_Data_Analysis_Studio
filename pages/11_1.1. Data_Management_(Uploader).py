import streamlit as st
import pandas as pd
import os
import numpy as np

# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config()

def upload_file(data_type, upload_key):
    """
    ファイルのアップロードを行う関数
    """
    st.subheader(f"Upload: {data_type}", divider='rainbow')
    uploaded_file = st.file_uploader(f"Please upload the {data_type.lower()}.", type=['csv'], key=upload_key)
    return uploaded_file # アップロードされたファイルを返す

def process_data_upload_with_upload_key(data_type, save_directory, upload_key):
    """
    アップロードされたファイルの処理を行う関数
    """
    uploaded_file = upload_file(data_type, upload_key)
    
    if uploaded_file is not None:

        df = func.load_data(uploaded_file, reduce_data=False)
        st.subheader(f"The {data_type} Uploaded:")
        st.dataframe(df)
        st.write(f"Shape of the data: {df.shape}")
        
        if data_type == "Operating Data":
            st.subheader("Statistical Summary:")
            st.dataframe(df.describe())
        
        func.save_data(df, data_type, save_directory)

# タイトルの設定
st.title('Data Management: Uploader')

# アップロードタイプの選択
upload_type = st.selectbox("Select the type of data to upload:", 
                           ["1_Operating Data", "2_Design Information"])

if upload_type == "1_Operating Data":
    process_data_upload_with_upload_key("Operating Data", var.operating_dir, "operating_data")
elif upload_type == "2_Design Information":
    # process_data_upload_with_upload_key("Tag Information", var.tag_dir, "tag_info")
    process_data_upload_with_upload_key("Design Information", var.design_dir, "design_info")
