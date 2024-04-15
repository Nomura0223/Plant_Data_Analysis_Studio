import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# ユーザー定義のライブラリをインポート
from library import variables as var
from library import functions as func
from library import config
config.set_page_config(layout="wide")

import os
from glob import glob

def plot_learning_curve(estimator, X, y, ax, title="Learning Curve"):
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=10, n_jobs=-1,
        train_sizes=np.linspace(.1, 1.0, 5),
        scoring="neg_mean_squared_error"
    )

    train_scores_mean = -np.mean(train_scores, axis=1)
    test_scores_mean = -np.mean(test_scores, axis=1)

    ax.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training error")
    ax.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation error")
    ax.set_title(title)
    ax.set_xlabel("Training examples")
    ax.set_ylabel("Mean Squared Error")
    ax.legend(loc="best")
    return ax

# 関数の定義
def select_file(directory):
    """
    ディレクトリからファイルを選択する関数
    """
    files = glob(os.path.join(directory, '*.csv'))
    if files:
        selected_file = st.selectbox("Select a file:", files)
        return selected_file # 選択されたファイルのパスを返す
    else:
        st.write("No files found.")
        return None


st.title("Diabetes Progression Prediction with Regression Models")


# データのロードと前処理
selected_file = select_file(var.operating_dir)
if selected_file:
    # ページをリロード
    df = func.load_data(selected_file, reduce_data=False)
    # st.dataframe(df)

# データを表示
if st.checkbox("Show data"):
    st.write(df)

# 説明変数と目的変数の選択
all_columns = df.columns.tolist()
inputs = st.multiselect("Select input features", all_columns, default=all_columns[:-1])
output = st.selectbox("Select target variable", all_columns, index=len(all_columns) - 1)

# モデル選択
model_type = st.sidebar.selectbox("Select model type", ["Linear Regression", "Random Forest Regression"])

# データの分割
test_size = st.sidebar.slider("Test Size (%)", min_value=10, max_value=50, value=20, step=5) / 100
if inputs and output:
    X_train, X_test, y_train, y_test = train_test_split(df[inputs], df[output], test_size=test_size, random_state=42)

    # モデルの訓練
    if model_type == "Linear Regression":
        model = LinearRegression()
    elif model_type == "Random Forest Regression":
        n_estimators = st.sidebar.slider("Number of trees", 10, 100, 50, 10)
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    
    model.fit(X_train, y_train)

    # モデルの評価
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # 評価結果の表示
    st.subheader("Model Performance")
    st.write(f"Mean Squared Error (MSE): {mse}")
    st.write(f"R-squared (R2): {r2}")

    # 学習曲線の表示
    st.subheader("Learning Curve")
    fig, ax = plt.subplots()
    plot_learning_curve(model, X_train, y_train, ax)
    st.pyplot(fig)

    # 予測と実際の値の比較
    st.subheader("Comparison of Predicted and Actual Values")
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.5)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')
    ax.set_title('Actual vs Predicted')
    st.pyplot(fig)

    # 元データと予測結果のプロット
    st.subheader("Plot of Predicted vs Actual Data Over Index")
    fig, ax = plt.subplots()
    ax.plot(y_test.reset_index(drop=True), label='Actual Data')
    ax.plot(pd.Series(y_pred, index=y_test.index).reset_index(drop=True), label='Predicted Data')
    ax.set_title("Actual vs Predicted Data")
    ax.set_xlabel("Index")
    ax.set_ylabel(output)
    ax.legend()
    st.pyplot(fig)
