import streamlit as st
import pandas as pd
import os

# 共通のファイル処理関数
def handle_file_upload(data_type, save_directory, upload_key):
    st.markdown(f"## {data_type}")
    uploaded_file = st.file_uploader(f"Please upload the {data_type.lower()}.", type=['csv'], key=upload_key)
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, header=0, index_col=0)
        st.write(f"The {data_type} Uploaded:")
        st.dataframe(df)
        st.write(f"Shape of the data: {df.shape}")
        # "Operating Data"の場合、Shapeとdescribe情報を表示
        if data_type == "Operating Data":
            st.write("Statistical Summary:")
            st.dataframe(df.describe())

        # 保存ファイル名の入力
        save_file_name = st.text_input(f"Type file name for {data_type.lower()}")
        
        # ファイル保存処理
        if st.button(f"Save {data_type}"):
            save_path = os.path.join(save_directory, save_file_name + ".csv")
            df.to_csv(save_path, index=True)
            st.success(f"{data_type} file has been saved to {save_path}.")

# タイトルの設定
st.title('Data Uploader')

# アップロードタイプの選択
upload_type = st.selectbox("Select the type of data to upload:", 
                           ["1_Operating Data", "2_Tag Information"])

if upload_type == "1_Operating Data":
    handle_file_upload("Operating Data", "./data/operating_data/", "operating_data")
elif upload_type == "2_Tag Information":
    handle_file_upload("Tag Information", "./data/tag_info/", "tag_info")
