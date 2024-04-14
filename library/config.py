import streamlit as st

# ページの設定
def set_page_config(layout = "centered"):
    st.set_page_config(
        page_title = "Plant Data Analysis Studio",
        page_icon = "📊",
        layout = layout,
        # initial_sidebar_state = "expanded",
    )


