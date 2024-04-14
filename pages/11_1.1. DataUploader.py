import streamlit as st
import pandas as pd
import os
import numpy as np

def upload_file(data_type, upload_key):
    """
    ファイルのアップロードを行う関数
    """
    st.subheader(f"Upload: {data_type}", divider='rainbow')
    uploaded_file = st.file_uploader(f"Please upload the {data_type.lower()}.", type=['csv'], key=upload_key)
    return uploaded_file

def load_data(file_path, reduce_data=False):
    """
    データのロードと前処理
    """
    try:
        # 日付時刻形式に変換を試みる
        df = pd.read_csv(file_path, header=0, parse_dates=[0], index_col=0)
    except (ValueError, TypeError):
        # 変換が失敗した場合は通常のインデックスとして読み込む
        df = pd.read_csv(file_path, header=0, index_col=0)
    
    if reduce_data:
        # データが多い場合は間引いて表示
        num_rows = len(df)
        interval = max(1, np.floor(num_rows / 100).astype(int))
        df = df.iloc[::interval, :]
        
    return df

def save_data(df, data_type, save_directory):
    """
    データの保存を行う関数
    """
    st.subheader(f"Save: {data_type}", divider='rainbow')
    save_file_name = st.text_input(f"Type file name for {data_type.lower()}")
    
    if st.button(f"Save {data_type}"):
        save_path = os.path.join(save_directory, save_file_name + ".csv")
        df.to_csv(save_path, index=True)
        st.success(f"{data_type} file has been saved to {save_path}.")

def process_data_upload(data_type, save_directory, upload_key):
    """
    アップロードされたファイルの処理を行う関数
    """
    uploaded_file = upload_file(data_type, upload_key)
    
    if uploaded_file is not None:
        # # ユーザーがデータ間引きを選択できるようにする
        # reduce_data = st.checkbox("Reduce data (to improve performance)", value=False)

        df = load_data(uploaded_file, reduce_data=False)
        st.subheader(f"The {data_type} Uploaded:")
        st.dataframe(df)
        st.write(f"Shape of the data: {df.shape}")
        
        if data_type == "Operating Data":
            st.subheader("Statistical Summary:")
            st.dataframe(df.describe())
        
        save_data(df, data_type, save_directory)

# タイトルの設定
st.title('Data Uploader')

# アップロードタイプの選択
upload_type = st.selectbox("Select the type of data to upload:", 
                           ["1_Operating Data", "2_Tag Information"])

if upload_type == "1_Operating Data":
    process_data_upload("Operating Data", "./data/operating_data/", "operating_data")
elif upload_type == "2_Tag Information":
    process_data_upload("Tag Information", "./data/tag_info/", "tag_info")
