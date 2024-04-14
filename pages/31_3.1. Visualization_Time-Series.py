import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from glob import glob
import plotly.graph_objs as go

# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config()


# データのロードと前処理
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


# データの可視化
def drawGraphImages(df, tag_info):
    for i, tag in enumerate(df.columns):
        x = df.index
        y = df[tag]

        fig = plt.figure(figsize=(15, 3))
        ax1 = fig.add_axes((0, 0, 0.79, 1))
        ax2 = fig.add_axes((0.82, 0, 0.1, 1 ), sharey=ax1)
        ax3 = fig.add_axes((0.95, 0, 0.05, 1 ), sharey=ax1)
        ax1.set_title(label=f"[{i+1}] {tag_info.loc[i, 'Tag']} | {tag_info.loc[i, 'Description']} | {tag_info.loc[i, 'Unit']} | mean={y.mean():.2f}, std={y.std():.2f}, min={y.min():.2f}, 25%={y.quantile(0.25):.2f}, 50%={y.quantile():.2f}, 75%={y.quantile(0.75):.2f}, max={y.max():.2f}", loc='left')

        # ax1.set_title(label=f"[{i+1}] {tag} | mean={y.mean():.2f}, std={y.std():.2f}, min={y.min():.2f}, max={y.max():.2f}", loc='left')
        ax1.plot(x, y, linestyle='solid', label='Operating', linewidth=2.0, color='#1d2088')
        ax1.grid(which = 'minor', axis = 'x', color = 'lightgrey', alpha = 0.8, linestyle = 'solid', linewidth = 0.5)

        # PFDの設計値をプロット
        ax1.axhline(y=tag_info.loc[i, 'Design Value'], linewidth=2.0, color='#ff4b00', label='Design')
        ax1.legend(loc='upper right', framealpha = 0.8, facecolor="white", frameon=True, handlelength=1, fontsize=10)


        ax2.hist(y.dropna(), bins=50, orientation='horizontal', color='#1d2088')
        ax2.axhline(y=tag_info.loc[i, 'Design Value'], linewidth=2.0, color='#ff4b00', label='Design')
        ax1.legend(loc='upper right', framealpha = 0.8, facecolor="white", frameon=True, handlelength=1, fontsize=10)
        ax3.boxplot(y.dropna(), widths=0.7)
        st.pyplot(fig)

# データの可視化
def drawGraphImages_interactive(df, tag_info):
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
    st.title('Visualization of Time Series Data')

    operating_data_directory = "./data/operating_data/"
    tag_info_directory = "./data/tag_info/"
    
    operating_files = glob(os.path.join(operating_data_directory, '*.csv'))
    tag_info_files = glob(os.path.join(tag_info_directory, '*.csv'))
    
    # ファイル選択のドロップダウンメニュー
    selected_file1 = st.selectbox("Please select the file for time series data:", operating_files, key="file1")
    selected_file2 = st.selectbox("Please select the file for tag information data:", tag_info_files, key="file2")

    if selected_file1 and selected_file2:
        df1 = load_data(selected_file1, reduce_data=True)
        df2 = pd.read_csv(selected_file2, header=0)
        st.subheader("View: Operating / Tag Information Data", divider='rainbow')

        st.write("Operating Data:")
        st.write(df1.head())

        st.write("Tag Information Data:")
        st.write(df2.head())

        st.subheader("Visualize: Time-Series Data", divider='rainbow')
        vis_type = st.radio("Select the visualization type:", ['Static', 'Interactive'])

        if st.button('Visualize Data'):
            if vis_type == 'Static':
                drawGraphImages(df=df1, tag_info=df2)
            else:
                drawGraphImages_interactive(df=df1, tag_info=df2)
            # drawGraphImages(df=df1, tag_info=df2)

if __name__ == "__main__":
    main()
