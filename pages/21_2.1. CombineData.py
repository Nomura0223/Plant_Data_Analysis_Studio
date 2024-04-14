import streamlit as st
import pandas as pd
import os
from glob import glob
from library import config
config.set_page_config()


# ディレクトリの指定
save_directory = "./data/operating_data/"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# タイトルの設定
st.title('Combine Operating Data')

# Streamlitのsession_stateの初期化
if 'combined_df' not in st.session_state:
    st.session_state.combined_df = None

# 指定ディレクトリ内のCSVファイルをリストアップ
files = glob(os.path.join(save_directory, '*.csv'))
selected_files = st.multiselect('Select files to combine:', files)

# 結合方向の選択
combine_direction = st.selectbox('Select combine direction:', ['Rows', 'Columns'])

# 結合処理
def combine_files():
    combined_df = None
    for i, file in enumerate(selected_files):
        df = pd.read_csv(file, index_col=0)
        if combined_df is None:
            combined_df = df
        else:
            if combine_direction == 'Rows':
                combined_df = pd.concat([combined_df, df], axis=0)
            else:  # Columns
                # 同一の列名が含まれる場合、新たに列名を定義して結合
                for col in df.columns:
                    if col in combined_df.columns:
                        df = df.rename(columns={col: f"{col}_{i}"})
                combined_df = pd.concat([combined_df, df], axis=1)
    st.session_state.combined_df = combined_df

if st.button('Combine Files', on_click=combine_files):
    if not selected_files or len(selected_files) < 2:
        st.error('Please select at least two files to combine.')
    else:
        st.success('Files combined successfully.')
        st.write('Combined Data Preview:')
        st.dataframe(st.session_state.combined_df)
        st.write(f'Shape of the combined data: {st.session_state.combined_df.shape}')
        st.write('Statistical Summary:')
        st.dataframe(st.session_state.combined_df.describe())

# 保存機能
save_file_name = st.text_input('Enter a name for the combined file (without extension)')
if st.button('Save Combined File') and st.session_state.combined_df is not None:
    if save_file_name:
        save_path = os.path.join(save_directory, save_file_name + ".csv")
        st.session_state.combined_df.to_csv(save_path)
        st.success(f'Combined file saved as {save_path}.')
    else:
        st.error('Please enter a file name.')
