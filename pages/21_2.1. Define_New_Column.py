import streamlit as st
import pandas as pd
import os
from glob import glob

# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config()


# ディレクトリの指定
save_directory = "./data/operating_data/"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# タイトルの設定
st.title('データ操作と保存')

# Streamlitのsession_stateの初期化
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

# CSVファイルを選択
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:")
    st.dataframe(st.session_state.df)

def add_new_column(dataframe, formula, new_column_name):
    """ Add a new column to the DataFrame based on the given formula. """
    try:
        dataframe[new_column_name] = pd.eval(formula, local_dict=dataframe)
        st.success("New column added successfully.")
        return dataframe
    except Exception as e:
        st.error(f"Error in calculation: {e}")
        return dataframe

# 列計算の入力
if st.session_state.df is not None and not st.session_state.df.empty:
    calc_formula = st.text_input("Enter your calculation formula (e.g., col1 + col2 * col3):")
    new_column_name = st.text_input("Enter the name for the new column:")
    
    if st.button("Add New Column"):
        st.session_state.df = add_new_column(st.session_state.df, calc_formula, new_column_name)
        st.dataframe(st.session_state.df)

# ファイルの保存
save_file_name = st.text_input("Enter a name for the new file (without extension):")
if st.button("Save File") and st.session_state.df is not None:
    if save_file_name:
        save_path = os.path.join(save_directory, save_file_name + ".csv")
        st.session_state.df.to_csv(save_path)
        st.success(f"File saved as {save_path}.")
    else:
        st.error("Please enter a file name.")
