import streamlit as st
import pandas as pd

# Streamlitアプリケーションのタイトル
st.title('CSVファイルのデータ加工と可視化')

# ファイルアップロードのウィジェット
uploaded_file = st.file_uploader("CSVファイルを選択してください", type=['csv'])

# ファイルがアップロードされたら処理開始
if uploaded_file is not None:
    # CSVファイルの読み込み
    df = pd.read_csv(uploaded_file)

    # データフレームの列名を取得
    columns = df.columns.tolist()
    
    # ユーザーが列を選択できるようにセレクトボックスを表示
    selected_column = st.selectbox("加工する列を選択してください", columns)
    
    # ユーザーが加工の種類を選択できるようにラジオボタンを表示
    operation = st.radio("実行する加工の種類を選択してください", ['平均値を計算', '最大値を探す', '最小値を探す'])
    
    # 選択された加工に応じて処理を実行
    if operation == '平均値を計算':
        result = df[selected_column].mean()
        st.write(f'{selected_column} の平均値: {result}')
    elif operation == '最大値を探す':
        result = df[selected_column].max()
        st.write(f'{selected_column} の最大値: {result}')
    elif operation == '最小値を探す':
        result = df[selected_column].min()
        st.write(f'{selected_column} の最小値: {result}')
