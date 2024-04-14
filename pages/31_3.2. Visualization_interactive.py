import streamlit as st
import pandas as pd
import numpy as np
import os
from glob import glob
import plotly.graph_objs as go

# データのロードと前処理
def load_data(file_path):
    try:
        # 日付時刻形式に変換を試みる
        df = pd.read_csv(file_path, header=0, parse_dates=[0], index_col=0)
    except (ValueError, TypeError):
        # 変換が失敗した場合は通常のインデックスとして読み込む
        df = pd.read_csv(file_path, header=0, index_col=0)
    
    # データが多い場合は間引いて表示
    num_rows = len(df)
    interval = max(1, np.floor(num_rows / 100).astype(int))
    df = df.iloc[::interval, :]
    return df

# データの可視化
def drawGraphImages(df, tag_info):
    for i, tag in enumerate(df.columns):
        x = df.index
        y = df[tag]

        # Plotlyグラフの作成
        trace1 = go.Scatter(x=x, y=y, mode='lines', name='Operating')
        trace2 = go.Scatter(x=[x.min(), x.max()], y=[tag_info.loc[i, 'Design Value'], tag_info.loc[i, 'Design Value']], mode='lines', name='Design', line=dict(color='firebrick', width=4, dash='dash'))
        
        layout = go.Layout(
            title=f"[{i+1}] {tag_info.loc[i, 'Tag']} | {tag_info.loc[i, 'Description']} | {tag_info.loc[i, 'Unit']}",
            xaxis=dict(title='Time'),
            yaxis=dict(title=tag),
            showlegend=True
        )
        
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        st.plotly_chart(fig)

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

        if st.button('データの可視化'):
            drawGraphImages(df=df1, tag_info=df2)

if __name__ == "__main__":
    main()
