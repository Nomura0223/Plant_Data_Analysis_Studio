import numpy as np
import pandas as pd
import os
import glob
import streamlit as st

# データのロードと前処理
def load_data(file_path, reduce_data=False):
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

# データの表示
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

# データの保存
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