import streamlit as st
import pandas as pd
import os
from glob import glob
import time

def select_file(directory):
    """
    ディレクトリからファイルを選択する関数
    """
    files = glob(os.path.join(directory, '*.csv'))
    if files:
        selected_file = st.selectbox("Select a file:", files)
        return selected_file
    else:
        st.write("No files found.")
        return None

def view_data(selected_file, data_type):
    """
    選択されたファイルのデータを表示する関数
    """
    if selected_file:
        df = pd.read_csv(selected_file, header=0, index_col=0)
        st.subheader(f"View: {data_type}", divider='rainbow')

        st.subheader(f"The {data_type} Selected:")
        st.dataframe(df)
        st.write(f"Shape of the data: {df.shape}")

        # データタイプが "Operating Data" の場合、統計概要を表示
        if data_type == "Operating Data":
            st.subheader("Statistical Summary:")
            st.dataframe(df.describe())

        return df
    else:
        return None

def delete_data(selected_file):
    """
    選択されたファイルを削除する関数
    """
    st.subheader(f"Delete: Selected Data", divider='rainbow')
    st.warning(f"Warning: This action is irreversible!")
    st.write("Please click the button to delete the selected file.")
    
    if selected_file and st.button("Delete", key="delete"):
        try:
            os.remove(selected_file)
            st.success(f"File {selected_file} has been deleted successfully.")
            time.sleep(3)
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error deleting file: {e}")

def manage_data_view(directory, data_type):
    """
    ファイル選択とデータ表示のプロセスを管理する関数
    """
    selected_file = select_file(directory)
    if selected_file:
        df = view_data(selected_file, data_type)
        delete_data(selected_file)

# タイトルの設定
st.title('Data Viewer')

# 閲覧タイプの選択
view_type = st.selectbox("Select the type of data to view:", ["1_Operating Data", "2_Tag Information"])

# データ管理プロセス
if view_type == "1_Operating Data":
    manage_data_view("./data/operating_data/", "Operating Data")
elif view_type == "2_Tag Information":
    manage_data_view("./data/tag_info/", "Tag Information")
