"""visualization related module"""

# library import 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import matplotlib.dates as mdates
from tqdm import tqdm

import glob
import os, shutil
import cv2
import img2pdf
from natsort import natsorted

# For Compressor Curve
from plotly.offline import iplot
from plotly.graph_objs import Scatter, Figure, Layout,Histogram

# 別のライブラリを参照
from preprocessing import outlier_removal

# 各Tagの可視化結果をpngファイルに出力する
def drawGraphImages(input_df, tag_info, start, end, savedir, outlier=False, rolling_window=0, show=False):

    # 画像の出力先ディレクトリの初期化
    try:
        shutil.rmtree(f"./{savedir}")
    except:
        pass

    # 画像の出力先ディレクトリの作成
    try: 
        os.makedirs(f"./{savedir}")
    except:
        pass

    df = input_df
    # df = input_df[start:end] # 可視化期間指定

    # データの可視化
    for i, tag in enumerate(tqdm(df.columns)):

        x = df.index
        y = df[tag]

        fig = plt.figure(figsize=(15, 3))
        ax1 = fig.add_axes((0, 0, 0.79, 1))
        ax2 = fig.add_axes((0.82, 0, 0.1, 1 ), sharey=ax1)
        ax3 = fig.add_axes((0.95, 0, 0.05, 1 ), sharey=ax1)

        ax1.set_title(label=f"[{i+1}] {tag_info.loc[i, 'Tag No.']} | {tag_info.loc[i, 'Description']} | {tag_info.loc[i, 'Unit']} | mean={y.mean():.2f}, std={y.std():.2f}, min={y.min():.2f}, 25%={y.quantile(0.25):.2f}, 50%={y.quantile():.2f}, 75%={y.quantile(0.75):.2f}, max={y.max():.2f}", loc='left')

        ax1.plot(x, y, linestyle='solid', label='Operating', linewidth=2.0, color='#1d2088')
        ax1.grid(which = 'minor', axis = 'x', color = 'lightgrey', alpha = 0.8, linestyle = 'solid', linewidth = 0.5)
        ax2.hist(y.dropna(), bins=50, orientation='horizontal', color='#1d2088')

        # 移動平均をプロット
        if rolling_window:
            ax1.plot(x, y.rolling(window=rolling_window, center=True).mean(), linestyle='solid', label=str(rolling_window)+"row_Rolling", linewidth=2.0, color='#ff4b00', alpha=0.75)
            # ax1.set_ylim(y_min-(y_max-y_min)*0.05, y_max+(y_max-y_min)*0.05)
            ax2.hist(y.dropna().rolling(window=rolling_window, center=True).mean(), bins=50, orientation='horizontal', color='#ff4b00', alpha=0.75)

        ax1.legend(loc='upper right', framealpha = 0.8, facecolor="white", frameon=True, handlelength=1, fontsize=10)
        ax3.boxplot(y.dropna(), widths=0.7)
        plt.savefig(f"{savedir}/plot{i+1}.png", bbox_inches='tight', dpi=150) 
        if show:
            plt.show()
        plt.close(fig)  # インラインで非表示

def drawGraphImages_withRollingData(input_df, column_list, tag_info, savedir, rolling_window=0, show=False):

    # 画像の出力先ディレクトリの初期化
    try:
        shutil.rmtree(f"./{savedir}")
    except:
        pass

    # 画像の出力先ディレクトリの作成
    try: 
        os.makedirs(f"./{savedir}")
    except:
        pass

    # df = input_df
    df = input_df.copy()
    # df = input_df[start:end] # 可視化期間指定

    # データの可視化
    for i, tag in enumerate(tqdm(column_list)):

        x = df.index
        y = df[tag]
        
        if rolling_window:
            tag2 = tag + f"_{rolling_window}_Rolling"
            y2 = df[tag2]
        
        fig = plt.figure(figsize=(15, 3))
        ax1 = fig.add_axes((0, 0, 0.79, 1))
        ax2 = fig.add_axes((0.82, 0, 0.1, 1 ), sharey=ax1)
        ax3 = fig.add_axes((0.95, 0, 0.05, 1 ), sharey=ax1)

        ax1.set_title(label=f"[{i+1}] {tag_info.loc[i, 'Tag No.']} | {tag_info.loc[i, 'Description']} | {tag_info.loc[i, 'Unit']} | mean={y.mean():.2f}, std={y.std():.2f}, min={y.min():.2f}, 25%={y.quantile(0.25):.2f}, 50%={y.quantile():.2f}, 75%={y.quantile(0.75):.2f}, max={y.max():.2f}", loc='left')

        ax1.plot(x, y, linestyle='solid', label='Operating', linewidth=2.0, color='#1d2088')
        ax1.grid(which = 'minor', axis = 'x', color = 'lightgrey', alpha = 0.8, linestyle = 'solid', linewidth = 0.5)
        # PFDの設計値をプロット
        # ax1.axhline(y=tag_info.loc[i, 'Design Value'], linewidth=2.0, color='#ff4b00', label='Design')

        ax2.hist(y.dropna(), bins=50, orientation='horizontal', color='#1d2088')

        if rolling_window:
            # 移動平均をプロット
            ax1.plot(x, y2, linestyle='solid', label=str(rolling_window)+"row_Rolling", linewidth=2.0, color='#ff4b00', alpha=0.75)
            # ax1.set_ylim(y_min-(y_max-y_min)*0.05, y_max+(y_max-y_min)*0.05)
            ax2.hist(y2, bins=50, orientation='horizontal', color='#ff4b00', alpha=0.75)

        ax1.legend(loc='upper right', framealpha = 0.8, facecolor="white", frameon=True, handlelength=1, fontsize=10)
        ax3.boxplot(y.dropna(), widths=0.7)
        plt.savefig(f"{savedir}/plot{i+1}.png", bbox_inches='tight', dpi=150) 
        if show:
            plt.show()
        plt.close(fig)  # インラインで非表示


# 各Tagの可視化結果をCombine (.png) それらを結合してpdfファイルに出力する。      
def conbineGraphImages(imgdir, outputname):
    combined_dir = imgdir+"_combined"

    # 画像の出力先ディレクトリの初期化
    try:
        shutil.rmtree(combined_dir)
    except:
        pass

    # 画像の出力先ディレクトリの作成
    try: 
        os.makedirs(combined_dir)
    except:
        pass
    
    # 画像一覧を取得
    imgs_list = glob.glob(imgdir + '\*')
    # 結合する画像のサイズが合っていないとエラーになるため、画像サイズを合わせる
    # plot1をベースサイズとする
    img_base = cv2.imread(f"{imgdir}/plot1.png")
    h1, w1, ch1 = img_base.shape[:3]
    # 画像ファイルのリスト
    v_list = []
    # 画像サイズをベースサイズに合わせて、リストに格納
    for i in range(len(imgs_list)):
        if i == 0:
            v_list.append(img_base)
        else:
            img_add = cv2.imread(f"{imgdir}/plot{i+1}.png")
            img_add = cv2.resize(img_add, (w1, h1))
            v_list.append(img_add)
    # 1ページに含める画像数
    n = 6
    # n個の画像ごとに結合して1ページを作成
    page = 0
    for i in tqdm(range(0, len(v_list), n)):
        # リストの画像ファイルを縦に結合
        image_v = cv2.vconcat(v_list[i: i+n])
        # 結合した画像のファイル名を指定
        image_v_name = f"{combined_dir}/page{page}.png"
        # 結合した画像データの書き出し
        cv2.imwrite(image_v_name, image_v)
        page += 1
    # 画像一覧を取得
    pages_list = list(glob.glob(combined_dir + '\*'))
    # PDFファイルを出力
    outputpath = f"Outputs/{outputname}.pdf"
    with open(outputpath,"wb") as f:
        f.write(img2pdf.convert([str(i) for i in natsorted(pages_list) if ".png" in i]))
        
    
# Compressor Curve 描画用
def scatterHist(df, x_tag, y_tag, z_tag):

    x_data = df[x_tag]
    y_data = df[y_tag]
    z_data = df[z_tag]

    #Create Graph Object
    scat = Scatter(
        # name="Scatter",
        x = x_data,
        y = y_data,
        mode = 'markers',
        marker=dict(size=3,
            color=z_data,          
            colorscale='Rainbow',
            showscale=True)
    )
    hist_x = Histogram(
        # name="Histogram_X",
        x = x_data,
        yaxis='y2',
    )
    hist_y = Histogram(
        # name="Histogram_Y",
        y = y_data,  
        xaxis='x2'
    )

    data = [scat,hist_x,hist_y]

    layout = Layout(
        # title = "散布図+ヒストグラム",

        width=800,
        height=600,
        showlegend=False,
        xaxis=dict(
            title=x_tag,
            domain=[0, 0.85],
            showgrid=True
        ),
        yaxis=dict(
            title=y_tag,
            domain=[0, 0.85],
            showgrid=True
        ),
        xaxis2=dict(
            domain=[0.85, 1],
        ),
        yaxis2=dict(
            domain=[0.85, 1],
        )
    )
    fig = Figure(data=data, layout=layout)
    iplot(fig)

def scatterHist_savefig(df, x_tag, y_tag, z_tag, savedir):

    # ディレクトリ作成
    try: 
        os.mkdir(f"./{savedir}")
    except:
        pass

    x_data = df[x_tag]
    y_data = df[y_tag]
    z_data = df[z_tag]

    #Create Graph Object
    scat = Scatter(
        # name="Scatter",
        x = x_data,
        y = y_data,
        mode = 'markers',
        marker=dict(size=3,
            color=z_data,          
            colorscale='Rainbow',
            showscale=True)
    )
    hist_x = Histogram(
        # name="Histogram_X",
        x = x_data,
        yaxis='y2',
    )
    hist_y = Histogram(
        # name="Histogram_Y",
        y = y_data,  
        xaxis='x2'
    )

    data = [scat,hist_x,hist_y]

    layout = Layout(
        # title = "散布図+ヒストグラム",

        width=800,
        height=600,
        showlegend=False,
        xaxis=dict(
            title=x_tag,
            domain=[0, 0.85],
            showgrid=True
        ),
        yaxis=dict(
            title=y_tag,
            domain=[0, 0.85],
            showgrid=True
        ),
        xaxis2=dict(
            domain=[0.85, 1],
        ),
        yaxis2=dict(
            domain=[0.85, 1],
        )
    )
    fig = Figure(data=data, layout=layout)
    fig.write_image(savedir + "/" + x_tag + y_tag + ".png")
    # iplot(fig)

def combine_images(imagedir, outputname):
    # 画像一覧を取得
    pages_list = list(glob.glob(imagedir + '/*'))
    # PDFファイルを出力
    outputpath = f"Outputs/{outputname}.pdf"
    with open(outputpath,"wb") as f:
        f.write(img2pdf.convert([str(i) for i in natsorted(pages_list) if ".png" in i]))   
