import streamlit as st
import pandas as pd
import joblib

# モデルと設定のロード
model_path = "saved_model.joblib"
model, inputs, output, stats = joblib.load(model_path)

st.title("Case Study: Simulate Different Scenarios with the Loaded Model")
st.write("Adjust the input features based on the statistical defaults to see how the predicted output changes.")

# 入力用のフォームを作成
with st.form("input_form"):
    input_data = {}
    # 入力ボックスを4列に分割して配置
    cols = st.columns(4)
    col_index = 0
    
    for feature in inputs:
        # ユーザーからの入力を受け取るためのフォーム要素を設定
        # 各統計値を使用してフォームを設定
        min_val = stats[feature]['min']
        max_val = stats[feature]['max']
        mean_val = stats[feature]['mean']
        with cols[col_index]:
            value = st.number_input(f"Set value for {feature}", min_value=min_val, max_value=max_val, value=mean_val)
            input_data[feature] = value
        col_index = (col_index + 1) % 4  # 次の列へ移動

    submit_button = st.form_submit_button(label='Predict')

    # 予測実行
    if submit_button:
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)
        # 出力結果の強調表示
        st.markdown(f"### Predicted {output}: `{prediction[0]}`", unsafe_allow_html=True)
