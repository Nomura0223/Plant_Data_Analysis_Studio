import numpy as np
import pandas as pd
import os

# Variables
column_list = [
    '給気風量', '給気静圧', '給気温度', '混錬品温度', '排気ﾌｧﾝ出力値', 'SD出口温度', '乾燥製品温度', '排気静圧',
    '排気温度', '排気湿度', '吸込み空気温度', '吸込み空気湿度', '2次ｴｱｰ温度', 'ﾌｨｰﾀﾞ供給量', '水分値',
    '粒度分布D50', 'ｴｸｽﾄﾙｰﾀﾞ回転数', 'ｴｸｽﾄﾙｰﾀﾞ電流値', '整粒機回転数', '整粒機電流値',
    'ｴｸｽﾄﾙｰﾀﾞﾄﾙｸ値', '液流量1', '液流量2', 'かさ密度', '最小オリフィス径', '収量', '不良品',
    '液流量1/2']

# Make directory
def make_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Excelファイルの読み込み
def read_excel_as_df (sheet_name, path):
    excel_books = pd.ExcelFile(path)
    df = excel_books.parse(sheet_name, header=None)
    return df

# データの整形
def data_formatting(df):
    df.iloc[:, 0] = df.iloc[:, 0].str.replace('/', '-')
    df["DATETIME"] = df.iloc[:, 0] + " "+ df.iloc[:, 1]
    df = df.iloc[:,3:]
    columns = df.iloc[1,:].tolist()
    columns[-1] = "DATETIME"
    df.columns = columns
    # 不要な行の削除
    df.drop(df.index[0:5], inplace=True)
    df["DATETIME"] = pd.to_datetime(df["DATETIME"])
    df.set_index('DATETIME', inplace=True)
    # 時間で昇順にソート
    df.sort_index(inplace=True)
    # 型変換
    df = df.astype('float64')
    # 元データの切れ目を認識するためにデータの最初と最後欠損値に変換
    df.iloc[0, :] = np.nan
    df.iloc[-1, :] = np.nan
    return df

# 新規タグの追加
def add_new_tags(df):
    
    # 1_良品/不良品
    condition_dia = (df["粒度分布D50"] >= 180) & (df["粒度分布D50"] <= 240)
    condition_moisture = df["水分値"] <= 2.5
    df["不良品"] = 1
    df.loc[condition_dia & condition_moisture, "不良品"] = 0

    # 2_液流量1/2
    df.loc[df["液流量2"] <= 1, "液流量2"] = 1 # 液流量2が0の場合、0除算になるため1に置換
    df["液流量1/2"] = df["液流量1"] / df["液流量2"]

    # 3_粒度分布判定
    df["粒度分布判定"] = "good"
    df.loc[df["粒度分布D50"] > 240, "粒度分布判定"] = "larger"
    df.loc[df["粒度分布D50"] < 180, "粒度分布判定"] = "smaller"
 
    return df

# 移動平均の追加
def add_moving_average(df, tag_list, window): # tag_list=['tag1', 'tag2', ...] or df.columns, window=75
    for tag in tag_list:
        df[f'{tag}_{window}_Rolling'] = df[tag].rolling(window=window, center=True).mean()
    return df

# 前処理
def prep_df(sheet_name, path):
    df = read_excel_as_df(sheet_name, path)
    df = data_formatting(df)
    df = add_new_tags(df)
    # df = add_moving_average(df, columns=df.columns, 75) # 移動平均追加
    return df


# 前処理
def data_preprocessing(df):
    df_preprocessed = df.copy()

    print("総データ数：", len(df_preprocessed))

    #1 '給気風量'
    tag = '給気風量'
    limit = 6.0
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] == limit))
    df_preprocessed[tag] = limit # ほぼ一定値のため一定値で補完

    #10 '排気湿度'
    tag = '排気湿度'
    limit = 10 # old_11.5
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] >= limit))
    df_preprocessed.loc[df_preprocessed[tag] < limit, tag] = np.nan # limit未満のデータを欠損値に変換

    #14 'ﾌｨｰﾀﾞ供給量'
    tag = 'ﾌｨｰﾀﾞ供給量'
    limit = 150
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] >= limit))
    df_preprocessed.loc[df_preprocessed[tag] < limit, tag] = np.nan # limit未満のデータを欠損値に変換

    #17 'ｴｸｽﾄﾙｰﾀﾞ回転数'
    tag = 'ｴｸｽﾄﾙｰﾀﾞ回転数'
    limit = 600 # old_700
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] >= limit))
    df_preprocessed.loc[df_preprocessed[tag] < limit, tag] = np.nan # limit未満のデータを欠損値に変換

    #18 'ｴｸｽﾄﾙｰﾀﾞ電流値'
    tag = 'ｴｸｽﾄﾙｰﾀﾞ電流値'
    limit = 0.7 # old_0.8
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] > limit))
    df_preprocessed.loc[df_preprocessed[tag] < limit, tag] = np.nan # limit未満のデータを欠損値に変換

    #19 '整粒機回転数'
    tag = '整粒機回転数'
    limit = 800
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] > limit))
    df_preprocessed.loc[df_preprocessed[tag] < limit, tag] = np.nan # limit未満のデータを欠損値に変換

    #20 '整粒機電流値'
    tag = '整粒機電流値'
    limit = 1
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] > limit))
    df_preprocessed.loc[df_preprocessed[tag] < limit, tag] = np.nan # limit未満のデータを欠損値に変換

    #22 '液流量1'
    tag = '液流量1'
    limit = 5
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] > limit))
    df_preprocessed.loc[df_preprocessed[tag] <= limit] = np.nan # limit未満のデータを欠損値に変換

    #23 '液流量2'
    tag = '液流量2'
    limit = 45 # old_54
    print(tag+" > "+str(limit)+":" ,sum(df_preprocessed[tag] > limit))
    df_preprocessed.loc[df_preprocessed[tag] <= limit] = np.nan # limit未満のデータを欠損値に変換

    return df_preprocessed


def merge_DataFrames (df, df_list=[]):
    merged_df = df.copy()
    for df_add in df_list:
        merged_df = pd.merge(merged_df, df_add, how="left")
    return merged_df

def outlier_removal(df, tag):
    upperlim = df[tag].quantile(0.75) + (df[tag].quantile(0.75) - df[tag].quantile(0.25)) * 1.5
    lowerlim = df[tag].quantile(0.25) - (df[tag].quantile(0.75) - df[tag].quantile(0.25)) * 1.5
    return df[(df[tag] <= upperlim) & (df[tag] >= lowerlim)]