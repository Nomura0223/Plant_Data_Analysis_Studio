import numpy as np
import pandas as pd
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