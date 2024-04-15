from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import streamlit as st
from glob import glob
import os

# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config(layout="wide")

# 関数の定義
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


# タイトルを追加
st.title("Visualization Dashboard")
st.write("This page provides interactive visualization capabilities for data analysis.")

st.subheader("Load: Data", divider='rainbow')

# データのロードと前処理
selected_file = select_file(var.operating_dir)
if selected_file:
    # ページをリロード
    df = func.load_data(selected_file, reduce_data=False)
    # df = pd.read_csv(selected_file, header=0)

    if st.checkbox("Show data"):
        st.dataframe(df)

st.subheader("Visualize:", divider='rainbow')

if st.button("Open Dashboard", key="open_dashboard"):
    # PyGWalkerとStreamlitの通信を確立する
    init_streamlit_comm()
 
    # PyGWalkerのレンダラーのインスタンスを取得する。このインスタンスをキャッシュすることで、プロセス内メモリの増加を効果的に防ぐことができます。
    @st.cache_resource
    def get_pyg_renderer() -> "StreamlitRenderer":
        # df = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")
        # アプリをパブリックに公開する場合、他のユーザーがチャートの設定ファイルに書き込めないように、デバッグパラメータをFalseに設定する必要があります。
        return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
    
    renderer = get_pyg_renderer()
    
    # データ探索インターフェースをレンダリングする。開発者はこれを使用してドラッグアンドドロップでチャートを作成できます。
    renderer.render_explore()