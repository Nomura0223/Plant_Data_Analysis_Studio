import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def load_data(uploaded_file, key="file1"):
    if uploaded_file is not None:
        if key == "file1":
            df = pd.read_csv(uploaded_file, header=0, index_col=0)
            # データが多い場合は間引いて表示
            num_rows = len(df) 
            interval = max(1, np.floor(num_rows / 100).astype(int))
            df = df.iloc[::interval, :]
            return df
        else:
            return pd.read_csv(uploaded_file, header=0)
    else:
        return None

def plot_data(df, column_name):
    fig, ax = plt.subplots()
    ax.plot(df.index, df[column_name])
    ax.set_xlabel('Index')
    ax.set_ylabel(column_name)
    st.pyplot(fig)

def drawGraphImages(df, tag_info):

    # データの可視化
    # for i, tag in enumerate(tqdm(df.columns)):
    for i, tag in enumerate(df.columns):

        x = df.index
        y = df[tag]

        fig = plt.figure(figsize=(15, 3))
        ax1 = fig.add_axes((0, 0, 0.79, 1))
        ax2 = fig.add_axes((0.82, 0, 0.1, 1 ), sharey=ax1)
        ax3 = fig.add_axes((0.95, 0, 0.05, 1 ), sharey=ax1)
        # print (tag_info.loc[i, 'Tag'])
        ax1.set_title(label=f"[{i+1}] {tag_info.loc[i, 'Tag']} | {tag_info.loc[i, 'Description']} | {tag_info.loc[i, 'Unit']} | mean={y.mean():.2f}, std={y.std():.2f}, min={y.min():.2f}, 25%={y.quantile(0.25):.2f}, 50%={y.quantile():.2f}, 75%={y.quantile(0.75):.2f}, max={y.max():.2f}", loc='left')

        ax1.plot(x, y, linestyle='solid', label='Operating', linewidth=2.0, color='#1d2088')
        ax1.grid(which = 'minor', axis = 'x', color = 'lightgrey', alpha = 0.8, linestyle = 'solid', linewidth = 0.5)
        ax2.hist(y.dropna(), bins=50, orientation='horizontal', color='#1d2088')


        ax1.legend(loc='upper right', framealpha = 0.8, facecolor="white", frameon=True, handlelength=1, fontsize=10)
        ax3.boxplot(y.dropna(), widths=0.7)
        st.pyplot(fig)
    # plt.show()





def main():
    st.title('CSVファイルのアップロードと可視化')

    # 2つのファイルアップロードウィジェット
    uploaded_file1 = st.file_uploader("時系列データのファイルを選択してください", type="csv", key="file1")
    uploaded_file2 = st.file_uploader("Tag情報データを選択してください", type="csv", key="file2")

    # 両方のファイルがアップロードされているか確認
    if uploaded_file1 is not None and uploaded_file2 is not None:
        df1 = load_data(uploaded_file1, key="file1")
        df2 = load_data(uploaded_file2, key="file2")


        st.write("時系列データ:")
        st.write(df1.head())
        
        # column_to_plot1 = st.selectbox('ファイル1で可視化する列を選択してください', options=df1.columns, key="select1")
        # plot_data(df1, column_to_plot1)
        
        st.write("Tag情報データ:")
        st.write(df2.head())
        
        # column_to_plot2 = st.selectbox('ファイル2で可視化する列を選択してください', options=df2.columns, key="select2")
        # plot_data(df2, column_to_plot2)

        if st.button('データの可視化'):
            drawGraphImages(df=df1, tag_info=df2)
    else:
        st.error("2つのファイルを両方アップロードしてください。")

if __name__ == "__main__":
    main()
