from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import numpy as np
import pandas as pd
import os
import streamlit as st
from glob import glob

# データのロードと前処理
def load_data(file_path, reduce_data=False):
    """
    データのロードと前処理
    """
    try:
        # 日付時刻形式に変換を試みる
        df = pd.read_csv(file_path, header=0, parse_dates=[0], index_col=0)
    except (ValueError, TypeError):
        # 変換が失敗した場合は通常のインデックスとして読み込む
        df = pd.read_csv(file_path, header=0, index_col=0)
    
    if reduce_data:
        # データが多い場合は間引いて表示
        num_rows = len(df)
        interval = max(1, np.floor(num_rows / 100).astype(int))
        df = df.iloc[::interval, :]
    return df


    """Configure the Streamlit page and sidebar for file selection."""
    # Adjust the width of the Streamlit page
    st.set_page_config(page_title="Data Analysis with PyGWalker", layout="wide")
    
    # Establish communication between PyGWalker and Streamlit
    init_streamlit_comm()
    
    # Display the title
    st.title("Exploaring Data Analysis with PyGWalker", anchor="top")
    
    # File selection in the sidebar
    operating_data_directory = "./data/operating_data/"
    operating_files = glob(os.path.join(operating_data_directory, '*.csv'))
    
    with st.sidebar:
        st.sidebar.title("Select File")
        selected_file = st.selectbox("Please select the file for analysis:", operating_files) 

        st.sidebar.title("Data Reduction")
        st.sidebar.markdown("Reduce the data to display:")
        reduce_data = st.sidebar.checkbox("Reduce Data", value=reduce_data)

        st.sidebar.button("Analyze Data", key="analyze_button")

    return load_data(selected_file, reduce_data)

def render_data_analysis(df):
    """Render the data analysis interface if the dataframe is not None."""
    if df is not None:
        # Get the PyGWalker renderer instance. This instance is cached to effectively prevent memory increase within the process.
        @st.cache_resource
        def get_pyg_renderer() -> "StreamlitRenderer":
            # Set the debug parameter to False when publishing the app publicly to prevent others from writing into the chart config file.
            return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
        
        renderer = get_pyg_renderer()
        renderer.render_explore()
    else:
        st.warning("Please upload a CSV file to proceed.")

def main():
    """Main function to execute the Streamlit app functionalities."""
    df = setup_streamlit()
    render_data_analysis(df)

if __name__ == "__main__":
    main()