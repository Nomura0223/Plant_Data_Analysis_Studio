import mysql.connector




### DB接続
cnx = mysql.connector.connect(
    host='mysql57.gsyn.sakura.ne.jp',
    user='gsyn',
    password='7DyybimA3xrP8xE',
    database='gsyn_gs_bm',
    )

### カーソル作成
cursor = cnx.cursor()

## query
sql = "SELECT * FROM operating_data"

## query実行    
cursor.execute(sql)

# import streamlit as st
# import pandas as pd
# import os





# # Directry
# save_directory = "./data/operating_data/"

# # タイトルの設定
# st.title('データの登録')

# st.markdown(
#     """
#     # Upload Operating Data
#     """
# )

# # ファイルアップロードのウィジェット
# uploaded_file = st.file_uploader("Please upload the operating data.", type=['csv'])


# if uploaded_file is not None:
#     # ファイルをDataFrameとして読み込み
#     df = pd.read_csv(uploaded_file)

#     # DataFrameの表示（省略可能）
#     st.write("The Operating Data Uploaded:")
#     st.dataframe(df)


#     # 保存ファイル名の入力
#     save_file_name = st.text_input("Type file name (with extension(e.g. '.csv')")

#     if st.button("Save"):
#         # 完全なパスを作成
#         save_path = os.path.join(save_directory, save_file_name)

#         # DataFrameをCSVファイルとして保存
#         edit_data.to_csv(save_path, index=False)

#         st.success(f"ファイルが {save_path} に保存されました。")
