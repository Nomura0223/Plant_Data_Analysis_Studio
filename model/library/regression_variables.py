"""
Regression Related Variables
"""

# Dataset Path
dataset_path = "../OperatingData/MTPC_Operating_Data.pkl"
dataset_preprocessed_path = "../OperatingData/MTPC_Operating_Data_Preprocessed.pkl"
dataset_preprocessed_rolling_path = "../OperatingData/MTPC_Operating_Data_Preprocessed_Rolling.pkl"
# Dataset Path (with Additional Data)
dataset_add_path = "../OperatingData/MTPC_Operating_Data_Added.pkl"
dataset_add_preprocessed_path = "../OperatingData/MTPC_Operating_Data_Added_Preprocessed.pkl"

# Train / Test Period for data separation
test_start = "2023-04-18 14:17:50" # Diameter: 313
test_end = "2023-06-05 11:26:30" # テストデータが全データの約10%となるように設定

test_start2 = "2023-06-05 11:43:40" 
test_end2 = "2023-09-01 11:27:24" 

test_start3 = "2023-09-05 14:10:54" 
test_end3 = "2023-09-12 11:12:40" 

test_start_list = [test_start, test_start2, test_start3]
test_end_list = [test_end, test_end2, test_end3]

# Input/Output Lists

list_X_all = [
    '給気風量', #1 変動小
    '給気静圧', #2 仮で削除
    '給気温度', #3 変動小
    '混錬品温度', #4　
    '排気ﾌｧﾝ出力値', #5 変動小
    'SD出口温度', #6 マルチコ #9
    '乾燥製品温度', #7 (仮) 無相関
    '排気静圧', #8 (仮) 無相関
    '排気温度', #9 マルチコ #6 (仮) 無相関
    '排気湿度', #10 (仮) 無相関
    '吸込み空気温度', #11 マルチコ #12
    '吸込み空気湿度', #12 マルチコ #11 
    '2次ｴｱｰ温度', #13 変動小
    'ﾌｨｰﾀﾞ供給量', #14 相関小
    # '水分値', #15
    # '粒度分布D50', #16
    'ｴｸｽﾄﾙｰﾀﾞ回転数', #17 変動小
    'ｴｸｽﾄﾙｰﾀﾞ電流値', #18 安定性が低いデータ
    '整粒機回転数', #19 変動小
    '整粒機電流値', #20 変動小
    'ｴｸｽﾄﾙｰﾀﾞﾄﾙｸ値', #21 安定性が低いデータ
    '液流量1', #22
    '液流量2', #23 (仮) 無相関
    'かさ密度', #24 データリーク
    '最小オリフィス径', #25 データリーク
    '収量' #26 データリーク
    ]

list_X_ImportanceCheck = [
    '給気静圧', #2 仮で削除
    '給気温度', #3 変動小
    '混錬品温度', #4　
    '排気ﾌｧﾝ出力値', #5 変動小
    'SD出口温度', #6 マルチコ #9
    '乾燥製品温度', #7 (仮) 無相関
    '排気静圧', #8 (仮) 無相関
    '排気温度', #9 マルチコ #6 (仮) 無相関
    '排気湿度', #10 (仮) 無相関
    '吸込み空気温度', #11 マルチコ #12
    '吸込み空気湿度', #12 マルチコ #11 
    'ﾌｨｰﾀﾞ供給量', #14 相関小
    'ｴｸｽﾄﾙｰﾀﾞ回転数', #17 変動小
    'ｴｸｽﾄﾙｰﾀﾞ電流値', #18 安定性が低いデータ
    'ｴｸｽﾄﾙｰﾀﾞﾄﾙｸ値', #21 安定性が低いデータ
    '液流量1', #22
    '液流量2', #23 (仮) 無相関
    ]

# rolling
list_X_ImportanceCheck_75_Rolling = [item + "_75_Rolling" for item in list_X_ImportanceCheck]


list_X_Candidates = [
    # '給気静圧', #2 仮で削除
    # '給気温度', #3 変動小 削除？
    '混錬品温度', #4　
    # '排気ﾌｧﾝ出力値', #5 変動小
    # 'SD出口温度', #6 マルチコ #9
    '乾燥製品温度', #7 (仮) 無相関
    # '排気静圧', #8 (仮) 無相関
    # '排気温度', #9 マルチコ #6 (仮) 無相関
    '排気湿度', #10 (仮) 無相関
    # '吸込み空気温度', #11 マルチコ #12
    '吸込み空気湿度', #12 マルチコ #11 
    'ﾌｨｰﾀﾞ供給量', #14 相関小
    # 'ｴｸｽﾄﾙｰﾀﾞ回転数', #17 変動小
    'ｴｸｽﾄﾙｰﾀﾞ電流値', #18 安定性が低いデータ
    'ｴｸｽﾄﾙｰﾀﾞﾄﾙｸ値', #21 安定性が低いデータ
    '液流量1', #22
    '液流量2', #23 (仮) 無相関
    ]

# After Parameter Search
list_Xa = [
    '混錬品温度', '排気湿度', '吸込み空気湿度', 'ﾌｨｰﾀﾞ供給量', 'ｴｸｽﾄﾙｰﾀﾞ電流値', '液流量1', '液流量2'
]

list_Xb = [
    '混錬品温度', '乾燥製品温度', '排気湿度', '吸込み空気湿度', 'ﾌｨｰﾀﾞ供給量', '液流量1', '液流量2'
]

list_Xa_rolling = [
    '混錬品温度', '排気湿度_75_Rolling', '吸込み空気湿度_75_Rolling', 'ﾌｨｰﾀﾞ供給量', 'ｴｸｽﾄﾙｰﾀﾞ電流値_75_Rolling', '液流量1', '液流量2'
]

# output tag (list_y)
list_y_class = ["不良品"]

list_y = [
    '粒度分布D50',
] 

list_y1 = [
    '水分値',
] 

list_y2 = [
    "水分値",
    '粒度分布D50',
] 

list_y2_75_Rolling = [item + "_75_Rolling" for item in list_y2]


list_y_Rolling = [
    '粒度分布D50_Rolling'
] 

# old for reference

list_X0 = [
    '給気風量', #1 変動小
    '給気静圧', #2 仮で削除
    '給気温度', #3 変動小
    '混錬品温度', #4　
    '排気ﾌｧﾝ出力値', #5 変動小
    'SD出口温度', #6 マルチコ #9
    '乾燥製品温度', #7 (仮) 無相関
    '排気静圧', #8 (仮) 無相関
    '排気温度', #9 マルチコ #6 (仮) 無相関
    '排気湿度', #10 (仮) 無相関
    '吸込み空気温度', #11 マルチコ #12
    '吸込み空気湿度', #12 マルチコ #11 
    '2次ｴｱｰ温度', #13 変動小
    'ﾌｨｰﾀﾞ供給量', #14 相関小
    # '水分値', #15
    # '粒度分布D50', #16
    'ｴｸｽﾄﾙｰﾀﾞ回転数', #17 変動小
    'ｴｸｽﾄﾙｰﾀﾞ電流値', #18 安定性が低いデータ
    '整粒機回転数', #19 変動小
    '整粒機電流値', #20 変動小
    'ｴｸｽﾄﾙｰﾀﾞﾄﾙｸ値', #21 安定性が低いデータ
    '液流量1', #22
    '液流量2', #23 (仮) 無相関
    ]


# Case1
list_X1 = [ 
    '混錬品温度', #4　
    'ｴｸｽﾄﾙｰﾀﾞ電流値', #18 安定性が低いデータ
    '液流量1', #22
    ]

list_X1_A = list_X1 + ["給気温度"]
list_X1_B = list_X1 + ["ﾌｨｰﾀﾞ供給量"]
list_X1_C = list_X1 + ["ｴｸｽﾄﾙｰﾀﾞ回転数"]
list_X1_D = list_X1 + ["液流量2"]


# Case2
list_X2 = [
    '給気温度', #3 変動小
    '混錬品温度', #4　
    'ﾌｨｰﾀﾞ供給量', #14 相関小
    'ｴｸｽﾄﾙｰﾀﾞ回転数', #17 変動小
    'ｴｸｽﾄﾙｰﾀﾞ電流値', #18 安定性が低いデータ
    '液流量1', #22
    '液流量2', #23 (仮) 無相関
    ]

list_X2_a = [item for item in list_X2 if item not in ["給気温度"]]
list_X2_b = [item for item in list_X2 if item not in ["混錬品温度"]]
list_X2_c = [item for item in list_X2 if item not in ["ﾌｨｰﾀﾞ供給量"]]
list_X2_d = [item for item in list_X2 if item not in ["ｴｸｽﾄﾙｰﾀﾞ回転数"]]
list_X2_e = [item for item in list_X2 if item not in ["ｴｸｽﾄﾙｰﾀﾞ電流値"]]
list_X2_f = [item for item in list_X2 if item not in ["液流量1"]]
list_X2_g = [item for item in list_X2 if item not in ["液流量2"]]

list_X2_A = list_X2 + ["排気ﾌｧﾝ出力値"]
list_X2_B = list_X2 + ["乾燥製品温度"]
list_X2_C = list_X2 + ["排気静圧"]
list_X2_D = list_X2 + ["排気湿度"]
list_X2_E = list_X2 + ["ｴｸｽﾄﾙｰﾀﾞﾄﾙｸ値"]

# Case3
list_X3 = [
    # '給気風量', #1 変動小
    # '給気静圧', #2 仮で削除
    '給気温度', #3 変動小
    '混錬品温度', #4　
    '排気ﾌｧﾝ出力値', #5 変動小
    # 'SD出口温度', #6 マルチコ #9
    '乾燥製品温度', #7 (仮) 無相関
    '排気静圧', #8 (仮) 無相関
    # '排気温度', #9 マルチコ #6 (仮) 無相関
    '排気湿度', #10 (仮) 無相関
    # '吸込み空気温度', #11 マルチコ #12
    # '吸込み空気湿度', #12 マルチコ #11 
    # '2次ｴｱｰ温度', #13 変動小
    'ﾌｨｰﾀﾞ供給量', #14 相関小
    # '水分値', #15
    # '粒度分布D50', #16
    # 'ｴｸｽﾄﾙｰﾀﾞ回転数', #17 変動小
    'ｴｸｽﾄﾙｰﾀﾞ電流値', #18 安定性が低いデータ
    # '整粒機回転数', #19 変動小
    # '整粒機電流値', #20 変動小
    'ｴｸｽﾄﾙｰﾀﾞﾄﾙｸ値', #21 安定性が低いデータ
    '液流量1', #22
    '液流量2', #23 (仮) 無相関
    # 'かさ密度', #24 データリーク
    # '最小オリフィス径', #25 データリーク
    # '収量' #26 データリーク
    ]

list_Xs = [
    list_X0,
    list_X1,
    list_X1_A, list_X1_B, list_X1_C, list_X1_D,
    list_X2_a, list_X2_b, list_X2_c, list_X2_d, list_X2_e, list_X2_f, list_X2_g,
    list_X2,
    list_X2_A, list_X2_B, list_X2_C, list_X2_D, list_X2_E,
    list_X3,
    ]


list_X1_75_Rolling = [item + "_75_Rolling" for item in list_X1]
list_X2_75_Rolling = [item + "_75_Rolling" for item in list_X2]
list_X3_75_Rolling = [item + "_75_Rolling" for item in list_X3]



