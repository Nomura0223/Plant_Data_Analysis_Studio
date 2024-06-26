import pandas as pd
import streamlit as st
from glob import glob
import os

# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config()

def select_file(directory):
    files = glob(os.path.join(directory, '*.csv'))
    if files:
        selected_file = st.selectbox("Select a file:", files)
        return selected_file
    else:
        st.write("No files found.")
        return None

st.title("Define New Column")
st.write("This page allows you to define a new column based on a calculation formula.")
st.subheader("Load: Data", divider='rainbow')

selected_file = select_file(var.operating_dir)
if selected_file:
    df = func.load_data(selected_file, reduce_data=False)
    if 'df' not in st.session_state:
        st.session_state.df = df
    st.dataframe(st.session_state.df)

def add_new_column(dataframe, formula, new_column_name):
    try:
        dataframe[new_column_name] = pd.eval(formula, local_dict=dataframe)
        st.success("New column added successfully.")
        return dataframe
    except Exception as e:
        st.error(f"Error in calculation: {e}")
        return dataframe

st.subheader("Define: New Column", divider='rainbow')
if 'df' in st.session_state and not st.session_state.df.empty:
    with st.form("my_form"):
        cols = st.columns([2, 1])
        with cols[0]:
            calc_formula = st.text_input("Enter your calculation formula (e.g., col1 + col2 * col3):")
        with cols[1]:
            new_column_name = st.text_input("Enter the name for the new column:")

        submitted = st.form_submit_button("Add New Column")
        if submitted:
            st.session_state.df = add_new_column(st.session_state.df, calc_formula, new_column_name)
            st.dataframe(st.session_state.df)

data_type = "Operating Data"
save_directory = var.operating_dir
func.save_data(st.session_state.df, data_type, save_directory)
