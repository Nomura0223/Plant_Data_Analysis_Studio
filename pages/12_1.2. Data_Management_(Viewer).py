import streamlit as st
import pandas as pd
import os
from glob import glob
import time

# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config()

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

def delete_data(selected_file):
    """
    選択されたファイルを削除する関数
    """
    st.subheader(f"Delete: Selected File", divider='rainbow')
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

def download_data(selected_file):
    """
    選択されたファイルをダウンロードする関数
    """
    with open(selected_file, "rb") as file:
        btn = st.download_button(
            label="Download data",
            data=file,
            file_name=os.path.basename(selected_file),
            mime='text/csv'
        )

def manage_data_view(directory, data_type):
    """
    ファイル選択とデータ表示、ダウンロード、削除のプロセスを管理する関数
    """
    selected_file = select_file(directory)
    if selected_file:
        func.view_data(selected_file, data_type)
        download_data(selected_file)
        delete_data(selected_file)

# タイトルの設定

st.title('Data Management: Viewer')
st.subheader("Load: Data", divider='rainbow')


# 閲覧タイプの選択
view_type = st.selectbox("Select the type of data to view:", ["1_Operating Data", "2_Design Information"])

# データ管理プロセス
if view_type == "1_Operating Data":
    manage_data_view(var.operating_dir, "Operating Data")
elif view_type == "2_Design Information":
    manage_data_view(var.design_dir, "Design Information")
