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
    1. **Data Management**: Upload CSV files and View/Delete uploaded data.
    2. **Preprocess**: Process uploaded data for analysis.
    3. **Visualization**: Use various tools to visualize/analyze data.
    4. **Machine Learning**: Build meachine learning model, and execute case study with models.

    ### Updates
    - April 12, 2024: 1st Deployment of Application.
    - April 16, 2024: Add Machine Learning (Regression) Function.
    - April 23, 2024: Add Machine Learning (Case Study) Function.
""")

st.header("", divider="blue")
