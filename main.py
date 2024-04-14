# ライブラリのインポート -------------------
import streamlit as st
from PIL import Image
from library import config

# ページの設定 ----------------------------
config.set_page_config()

# メイン画面 -------------------
st.title('Plant Data Analysis Studio', anchor='top')

image = Image.open('image.jpg')
st.image(image, use_column_width=True)

# サイドバーの設定
st.sidebar.success("Select pages above to start!")

# アプリケーション説明
st.markdown("""
    ### Overview
    Welcome to Plant Data Analysis Studio! This application is a data analysis platform for plant engineers. You can upload data, conduct analyses, and gain insights.

    ### Key Features
    - **Data Upload**: Upload CSV or Excel files and start analyzing immediately.
    - **Interactive Analysis Tools**: Use various tools to visualize and analyze data.
    - **Report Generation**: Export your analysis results as a report and share it.

    ### Updates
    - April 12, 2024: Added new visual analysis tools.
""")
