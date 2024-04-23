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

st.title("Visualization Dashboard")
st.write("This page provides interactive visualization capabilities for data analysis.")
st.subheader("Load: Data", divider='rainbow')

selected_file = select_file(var.operating_dir)
if selected_file:
    df = func.load_data(selected_file, reduce_data=False)
    if st.checkbox("Show data"):
        st.dataframe(df)

    st.subheader("Visualize:", divider='rainbow')
    if st.button("Open Dashboard", key="open_dashboard"):
        # PyGWalkerとStreamlitの通信を確立する
        init_streamlit_comm()
     
        # PyGWalkerのレンダラーのインスタンスを取得する。このインスタンスをキャッシュすることで、プロセス内メモリの増加を効果的に防ぐことができます。
        @st.cache_resource
        def get_pyg_renderer() -> "StreamlitRenderer":
            # データフレーム `df` をレンダラーに渡す
            return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
        
        renderer = get_pyg_renderer()
        
        # データ探索インターフェースをレンダリングする。開発者はこれを使用してドラッグアンドドロップでチャートを作成できます。
        renderer.render_explore()
