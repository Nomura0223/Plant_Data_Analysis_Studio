import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import mean_squared_error, r2_score
import plotly.graph_objs as go
import os
from glob import glob
import joblib  # joblibのインポート

# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config(layout="wide")

def plot_learning_curve(estimator, X, y, title="Learning Curve"):
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=10, n_jobs=-1,
        train_sizes=np.linspace(.1, 1.0, 5),
        scoring="neg_mean_squared_error"
    )

    train_scores_mean = -np.mean(train_scores, axis=1)
    test_scores_mean = -np.mean(test_scores, axis=1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=train_sizes, y=train_scores_mean, mode='lines+markers', name='Training error'))
    fig.add_trace(go.Scatter(x=train_sizes, y=test_scores_mean, mode='lines+markers', name='Validation error'))
    fig.update_layout(title=title, xaxis_title='Training examples', yaxis_title='Mean Squared Error')
    return fig

def select_file(directory):
    files = glob(os.path.join(directory, '*.csv'))
    if files:
        selected_file = st.selectbox("Select a file:", files)
        return selected_file
    else:
        st.write("No files found.")
        return None

st.title("Machine Learning: Build Regression Model")
st.write("This page allows you to build a machine learning model for regression analysis.")
st.subheader("Load: Data", divider='rainbow')

selected_file = select_file(var.operating_dir)
df = None
if selected_file:
    df = func.load_data(selected_file, reduce_data=False)

if df is not None and st.checkbox("Show data"):
    st.write(df)

st.subheader("Build: Model", divider='rainbow')
model = None
if df is not None:
    all_columns = df.columns.tolist()
    inputs = st.multiselect("Select input features", all_columns, default=all_columns[:-1])
    output = st.selectbox("Select target variable", all_columns, index=len(all_columns) - 1)

    model_type = st.selectbox("Select model type", ["Linear Regression", "Random Forest Regression"])
    test_size = st.slider("Test Size (%)", min_value=10, max_value=50, value=20, step=5) / 100

    if st.button("Build Model"):
        if inputs and output:
            X_train, X_test, y_train, y_test = train_test_split(df[inputs], df[output], test_size=test_size, random_state=42)
            
            if model_type == "Linear Regression":
                model = LinearRegression()
            elif model_type == "Random Forest Regression":
                n_estimators = st.slider("Number of trees", 10, 100, 50, 10)
                model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            st.subheader("Visualize: Model Performance", divider="rainbow")
            st.write(f"Mean Squared Error (MSE): {mse}")
            st.write(f"R-squared (R2): {r2}")

            col1, col2, col3 = st.columns(3)
            
            with col1:
                fig = plot_learning_curve(model, X_train, y_train)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=y_test, y=y_pred, mode='markers', name='Predicted vs Actual', marker=dict(color='LightSkyBlue', opacity=0.5)))
                fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], mode='lines', name='Ideal Line', line=dict(color='black', dash='dash')))
                fig.update_layout(title="Comparison of Predicted and Actual Values", xaxis_title="Actual", yaxis_title="Predicted", legend_title="Legend")
                st.plotly_chart(fig, use_container_width=True)

            with col3:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=np.arange(len(y_test)), y=y_test.reset_index(drop=True), mode='lines', name='Actual'))
                fig.add_trace(go.Scatter(x=np.arange(len(y_pred)), y=y_pred, mode='lines', name='Predicted'))
                fig.update_layout(title="Plot of Predicted vs Actual Data Over Index", xaxis_title="Index", yaxis_title=output)
                st.plotly_chart(fig, use_container_width=True)

            # モデルおよび設定の保存
            model_path = "saved_model.joblib"
            stats = df[inputs].agg(['mean', 'min', 'max']).to_dict()  # 統計情報を計算して辞書として保存
            joblib.dump((model, inputs, output, stats), model_path)
            st.success(f"Model, configuration, and statistics saved to {model_path}")

# # モデルが作成された後のシミュレーション部分
# if model:
#     st.subheader("Simulation: Adjust Input Features", divider="rainbow")

#     # 入力用のフォームを作成
#     with st.form("input_form"):
#         input_data = {}
#         for feature in inputs:
#             # 各説明変数の最小値と最大値をデータから取得して範囲を設定
#             min_val = df[feature].min()
#             max_val = df[feature].max()
#             step = (max_val - min_val) / 100  # ステップサイズを適切に設定
#             default_val = (max_val + min_val) / 2
#             input_data[feature] = st.number_input(f"Set value for {feature}", min_value=min_val, max_value=max_val, value=default_val, step=step)
        
#         submit_button = st.form_submit_button(label='Predict')

#         # 予測実行
#         if submit_button:
#             input_df = pd.DataFrame([input_data])
#             prediction = model.predict(input_df)
#             st.write(f"Predicted {output}: {prediction[0]}")
