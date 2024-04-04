import streamlit as st
import pandas as pd
import os
from glob import glob

# データ閲覧および削除機能の共通関数
def view_and_delete_data(data_type, save_directory):
    st.markdown(f"## View or Delete {data_type}")
    # 指定ディレクトリ内のCSVファイルをリストアップ
    files = glob(os.path.join(save_directory, '*.csv'))
    if files:
        selected_file = st.selectbox(f"Select a file to view or delete:", files)
        if st.button(f"View {data_type}"):
            df = pd.read_csv(selected_file, header=0, index_col=0)
            st.dataframe(df)
        
        # 選択したファイルを削除
        if st.button("Delete Selected File"):
            try:
                os.remove(selected_file)
                st.success(f"File {selected_file} has been deleted successfully.")
            except Exception as e:
                st.error(f"Error deleting file: {e}")
    else:
        st.write("No files found.")

# タイトルの設定
st.title('Data Viewer and Deleter')

# 閲覧タイプの選択
view_type = st.selectbox("Select the type of data to view or delete:", 
                         ["1_Operating Data", "2_Tag Information"])

if view_type == "1_Operating Data":
    view_and_delete_data("Operating Data", "./data/operating_data/")
elif view_type == "2_Tag Information":
    view_and_delete_data("Tag Information", "./data/tag_info/")
