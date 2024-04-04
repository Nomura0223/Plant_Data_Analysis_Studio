# ライブラリのインポート -------------------
import streamlit as st
# import google.generativeai as genai
from PIL import Image

# ページの設定 ----------------------------
st.set_page_config(
    page_title="Plant Data Analysis Studio",
    page_icon="🤖",
)

# メイン画面 -------------------

st.title('🤖 Plant Data Analysis Studio 🤖', anchor='top')

image = Image.open('image.jpg')
st.image(image, use_column_width=True)

st.sidebar.success("Select the functions above.")

st.markdown(
    """
    Plant Data Analysis Studio へようこそ！
    このアプリケーションは、プラントエンジニア向けデータ分析プラットフォームです。\n
    👈 サイドバーから実施したい業務プロセス処理を選択して、機能の例を体験下さい！
    """
)