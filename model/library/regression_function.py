"""regression related module"""

# library import 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import random as rn
import pickle

import tensorflow as tf
from tensorflow.python import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

def yyplot(y_true, y_pred):
    yvalues = np.concatenate([y_true.flatten(), y_pred.flatten()])
    ymin, ymax, yrange = np.amin(yvalues), np.amax(yvalues), np.ptp(yvalues)
    fig = plt.figure(figsize=(5, 5))
    plt.scatter(y_true, y_pred, s=1.0)
    plt.plot([ymin - yrange * 0.01, ymax + yrange * 0.01], [ymin - yrange * 0.01, ymax + yrange * 0.01], color="red", linestyle = "dashed")
    plt.xlim(ymin - yrange * 0.01, ymax + yrange * 0.01)
    plt.ylim(ymin - yrange * 0.01, ymax + yrange * 0.01)
    plt.xlabel('t: true value')
    plt.ylabel('y: predicted value')
    plt.title('True-Predicted Plot')
    plt.show()
    return fig

def learning_curve(history):
    fig = plt.figure(figsize=(10, 4))
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.title(label='Learning curve')
    plt.xlabel(xlabel='Epoch')
    plt.ylabel(ylabel='MSE')
    # plt.ylim(bottom=0.0, top=0.2)
    plt.legend()
    plt.yscale('log')
    plt.grid()    
    plt.show()
    return fig

def metrics(y_true, y_pred, show=True):
    metrics = [r2_score(y_true=y_true, y_pred=y_pred), 
               np.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred)), 
               mean_absolute_error(y_true=y_true, y_pred=y_pred)
              ]
    if show:
        print("r2:          %.4f" % metrics[0])
        print("rmse:        %.4f" % metrics[1])
        print("rmse / avg.: %.4f" % (metrics[1] / y_true.mean()))
        print("mae:         %.4f" % metrics[2])
        print("mae / avg.:  %.4f" % (metrics[2] / y_true.mean()))
    return metrics

def reset_seed(seed=0):
    os.environ['PYTHONHASHSEED'] = '0'
    rn.seed(seed) # random関数のシードを固定
    np.random.seed(seed) # numpyのシードを固定
    tf.random.set_seed(seed) # tensorflowのシードを固定
    
def outlier_removal(df, tag, IQR_range=1.5):
    upperlim = df[tag].quantile(0.75) + (df[tag].quantile(0.75) - df[tag].quantile(0.25)) * IQR_range
    lowerlim = df[tag].quantile(0.25) - (df[tag].quantile(0.75) - df[tag].quantile(0.25)) * IQR_range
    return df[(df[tag] <= upperlim) & (df[tag] >= lowerlim)]


def extract_neighborhood (df, df_original, tag, current_row, neighborhood_range):
    lower_lim = df_original.loc[current_row, tag] - neighborhood_range #case 4 下限: Current - 0.25%
    upper_lim = df_original.loc[current_row, tag] + neighborhood_range #caase 4 上限: Current + 0.25%
    return df[(df[tag] <= upper_lim) & (df[tag] >= lower_lim)]

def preprocess(df):
    df_shape_before = df.shape
    df = df[df["Done"] == True]
    df = df[df["Error"] == False]
    df = df[df["WB_MDT_Sim"] > 0.2]
    df = df[df["CB_MDT_Sim"] > 0.2]

    # Outlier Removal
    df = outlier_removal(df, "Spec_Power_Sim")
    df = outlier_removal(df, "WB_UA_Calc_Sim")
    df = outlier_removal(df, "CB_UA_Calc_Sim")
    df_shape_after = df.shape
    print("Preprocessed:",df_shape_before, "→", df_shape_after)
    return df

def save_models(model, sc_X, sc_y, directory):
    model.save(directory+"/model.h5")
    from pickle import dump    
    dump(sc_X, open(directory+'/sc_x.pkl', 'wb'))
    dump(sc_y, open(directory+'/sc_y.pkl', 'wb'))

def load_models(directory: str):
    model = load_model(directory+'/model.h5')
    sc_X = pickle.load(open(directory+'/sc_x.pkl', "rb"))
    sc_y = pickle.load(open(directory+'/sc_y.pkl', "rb"))
    return model, sc_X, sc_y
    
def makeModel (input_dim, output_dim, hidden_layer1_units=16, hidden_layer2_units=8, hidden_layer3_units=0, activation_func = "tanh", loss = 'mean_squared_error', dropout=0) -> Sequential():
    reg = Sequential()
    reg.add(Dense(units=hidden_layer1_units, input_dim=input_dim, activation=activation_func))
    if dropout:
        reg.add(Dropout(dropout))
    reg.add(Dense(units=hidden_layer2_units, activation=activation_func))
    if dropout:
        reg.add(Dropout(dropout))
    if hidden_layer3_units:
        reg.add(Dense(units=hidden_layer3_units, activation=activation_func))
        if dropout:
            reg.add(Dropout(dropout))
    reg.add(Dense(units=output_dim))
    opt = Adam(learning_rate=0.001)
    reg.compile(loss=loss, optimizer=opt)
    # reg.summary()
    return reg

def prediction(input_x, model, sc_x, sc_y):
    x_sc = sc_x.transform(input_x)
    y_pred_sc = model.predict(x_sc, batch_size=4096, verbose=False)
    y_pred = sc_y.inverse_transform(y_pred_sc)
    return y_pred

