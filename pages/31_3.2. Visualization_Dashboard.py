from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import streamlit as st
from glob import glob
import os

# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config()

# define variables
directory = "./data/operating_data/"

def select_file(directory):
    """
    ディレクトリからファイルを選択する関数
    """
    files = glob(os.path.join(directory, '*.csv'))
    if files:
        selected_file = st.selectbox("Select a file:", files)
        return selected_file # 選択されたファイルのパスを返す
    else:
        st.write("No files found.")
        return None


# Streamlitページの幅を調整する
st.set_page_config(
    layout="wide"
)
 
# PyGWalkerとStreamlitの通信を確立する
init_streamlit_comm()
 
# タイトルを追加
st.title("Visualization Dashboard")

# 設定
st.write("This is a dashboard for visualizing data using PyGWalker.")

# ファイル選択
st.title("Select File")
st.write("Please select the file for analysis.")

# データのロードと前処理
selected_file = select_file(directory)
if selected_file:
    df = pd.read_csv(selected_file, header=0, index_col=0)
    st.write(df.head())
    


# PyGWalkerのレンダラーのインスタンスを取得する。このインスタンスをキャッシュすることで、プロセス内メモリの増加を効果的に防ぐことができます。
@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    df = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")
    # アプリをパブリックに公開する場合、他のユーザーがチャートの設定ファイルに書き込めないように、デバッグパラメータをFalseに設定する必要があります。
    return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
 
renderer = get_pyg_renderer()
 
# データ探索インターフェースをレンダリングする。開発者はこれを使用してドラッグアンドドロップでチャートを作成できます。
renderer.render_explore()