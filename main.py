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

# st.header("", divider="blue")

st.markdown("""
    ### Overview
    Welcome to Plant Data Analysis Studio! This application is a data analysis platform for plant engineers. You can upload data, conduct analyses, and gain insights.

    ### Key Features
    - **Data Upload**: Upload CSV files and start analyzing immediately.
    - **Data Viewer**: View uploaded data, download files, and delete data.
    - **Interactive Data Analysis**: Use various tools to visualize and analyze data.
    - **Machine Learning**: Train and test machine learning models on your data.

    ### Updates
    - April 12, 2024: Added new visual analysis tools.
""")

st.header("", divider="blue")
