import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from glob import glob

# データのロードと前処理
def load_data(file_path):
    df = pd.read_csv(file_path, header=0, index_col=0)
    # データが多い場合は間引いて表示
    num_rows = len(df)
    interval = max(1, np.floor(num_rows / 100).astype(int))
    df = df.iloc[::interval, :]
    return df

# データの可視化
def drawGraph(df, tag, graph_type):
    x = df.index
    y = df[tag]

    if graph_type == 'Histogram':
        plt.figure(figsize=(10, 4))
        plt.hist(y.dropna(), bins=50, color='#1d2088')
        plt.title(f'Histogram of {tag}')
        st.pyplot(plt)

    elif graph_type == 'Jointplot':
        sns.jointplot(x=x, y=y, kind='hex', color='#1d2088')
        plt.suptitle(f'Jointplot of {tag}')
        st.pyplot(plt)

# メイン関数
def main():
    st.title('CSVファイルのアップロードと可視化')

    operating_data_directory = "./data/operating_data/"
    tag_info_directory = "./data/tag_info/"

    operating_files = glob(os.path.join(operating_data_directory, '*.csv'))
    tag_info_files = glob(os.path.join(tag_info_directory, '*.csv'))

    # ファイル選択のドロップダウンメニュー
    selected_file1 = st.selectbox("時系列データのファイルを選択してください", operating_files, key="file1")
    selected_file2 = st.selectbox("Tag情報データを選択してください", tag_info_files, key="file2")

    if selected_file1 and selected_file2:
        df1 = load_data(selected_file1)
        df2 = pd.read_csv(selected_file2, header=0)

        st.write("時系列データ:")
        st.write(df1.head())

        st.write("Tag情報データ:")
        st.write(df2.head())

        # グラフタイプの選択
        graph_type = st.selectbox("グラフタイプを選択してください", ['Histogram', 'Jointplot'])

        # Tagの選択
        tag = st.selectbox("Tagを選択してください", df1.columns)

        if st.button('データの可視化'):
            drawGraph(df=df1, tag=tag, graph_type=graph_type)

if __name__ == "__main__":
    main()
