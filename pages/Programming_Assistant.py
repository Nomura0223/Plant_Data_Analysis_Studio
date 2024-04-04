# ライブラリのインポート -------------------
import streamlit as st
import google.generativeai as genai
from PIL import Image

# ページの設定 ----------------------------
st.set_page_config(
    page_title="Programming Assistant",
    page_icon="🤖",
)

# APIキーの設定 -----------------------
genai.configure(api_key="AIzaSyDKS9IwFZSqnon9UXzRE6yWokgrwe-2cmQ")
model = genai.GenerativeModel('gemini-pro')

# サイド画面 ----------------------------------

st.sidebar.title('設定項目', anchor='sidebar')
st.sidebar.subheader('', divider="rainbow")

language = st.sidebar.selectbox('プログラミング言語:',
                list(["Python", "JavaScript", "html", "CSS", "その他"]))
if language == "その他":
    language = st.sidebar.text_input('その他:')

perpose = st.sidebar.selectbox('目的:',
                                 list(["コードの作成", "コードの修正", "コードの解説"]))
if perpose == "その他":
    perpose = st.sidebar.text_input('その他:')

description_dict = {"コードの作成": "作成したいコードについての説明を入力してください。",
        "コードの修正": "修正したいコードを入力してください。",
        "コードの解説": "解説してほしいコードを入力してください。"}

content = st.sidebar.text_area('内容:', placeholder=description_dict[perpose],   height=400)

st.sidebar.subheader('', divider="rainbow")

# メイン画面 -------------------

st.title('プログラミングアシスタント', anchor='top')

image = Image.open('robot_wide.png')
st.image(image, use_column_width=True)

st.markdown(
    """
    そのアプリではプログラミングの補助アプリです。サイドバーで設定した条件をもとに回答を生成します。
    設定が完了したら「作成」ボタンをクリックしてください！
    """
)


# ボタンの設定
col1, col2, col3 = st.columns(3)
with col2:
    button = st.button('作成', use_container_width=True)

st.subheader('', divider="rainbow")

# 命令文の作成
user_input = ""
user_input += f"プログラミング言語は「{language}」を使用。次の文章を踏まえて「{perpose}」をお願い致します。「{content}」"


# ボタンが押されたら
if button:
    if content != "":
        user_text = st.chat_message("user")
        user_text.write(user_input)
        with st.spinner('文章を作成中...'):
            response = model.generate_content(user_input)
        message = st.chat_message("ai")
        message.write(response.text)
        st.subheader('', divider="rainbow")
    else:
        st.error('設定項目の入力が完了しておりません。')
    
