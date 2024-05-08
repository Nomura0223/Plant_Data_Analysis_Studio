import streamlit as st
import pandas as pd
import joblib
from scipy.optimize import minimize

# モデルと設定のロード
model_path = "saved_model.joblib"
model, inputs, output, stats = joblib.load(model_path)

st.title("Machine Learning: Case Study")
st.write("This page allows you to simulate different scenarios with the loaded model and optimize the target variable.")

st.subheader("Input:", divider='rainbow')
st.write("Adjust the input features based on the statistical defaults to see how the predicted output changes and optimize the output.")

# 入力用のフォームを作成
with st.form("input_form"):
    input_data = {}
    cols = st.columns(4)
    col_index = 0
    
    for feature in inputs:
        min_val = stats[feature]['min']
        max_val = stats[feature]['max']
        mean_val = stats[feature]['mean']
        with cols[col_index]:
            value = st.number_input(f"Set value for {feature}", min_value=min_val, max_value=max_val, value=mean_val)
            input_data[feature] = value
        col_index = (col_index + 1) % 4  # 次の列へ移動
    
    # 予測ボタンと最適化ボタン
    col1, col2 = st.columns(2)
    with col1:
        submit_button = st.form_submit_button("Predict")
    with col2:
        optimize_button = st.form_submit_button("Optimize")
        # 最適化の方向を選択するためのラジオボタン
        optimize_direction = st.radio("Optimize target to:", ("Maximize", "Minimize"))

st.subheader("Output:", divider='rainbow')

# 予測実行
if submit_button:
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    st.subheader(f"Predicted {output}: `{format(prediction[0], '.2f')}`")  # 小数点以下2桁で表示

# 最適化実行
if optimize_button:
    # 目的関数
    def objective_function(x):
        df = pd.DataFrame([dict(zip(inputs, x))])
        pred = model.predict(df)
        return -pred if optimize_direction == "Maximize" else pred

    # 初期値
    initial_values = [stats[feature]['mean'] for feature in inputs]
    # 範囲
    bounds = [(stats[feature]['min'], stats[feature]['max']) for feature in inputs]

    # 最適化
    result = minimize(objective_function, initial_values, bounds=bounds, method='L-BFGS-B')
    
    if result.success:
        optimized_values = result.x
        optimized_prediction = model.predict([optimized_values])
        st.subheader(f"Optimized {output} ({optimize_direction}): `{format(optimized_prediction[0], '.2f')}`")  # 小数点以下2桁で表示
        
        # 更新された値を入力フォームに反映
        updated_data = {feature: format(value, '.2f') for feature, value in zip(inputs, optimized_values)}
        st.write("Updated input values for optimization:")
        st.json(updated_data)
    else:
        st.error("Optimization failed. Try different settings or check the model constraints.")
