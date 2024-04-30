import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def fix_col(df):
    l = list(df.columns)
    l1 = []
    for i in l:
        a= i.lower().replace(' ','_')
        a = a.replace('-','_')
        l1.append(a)
    d = dict(zip(l,l1))
    df.rename(d, axis=1, inplace=True)
    return df

def remove_outliers(df,col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3-q1                   # inter quirtile range quater 3 minus quater 1
    lb = q1 - 1.5*iqr                 # lower bound
    ub = q3 + 1.5*iqr                     # upper bound
    return df.loc[(df[col]>lb)&(df[col]<ub)]

