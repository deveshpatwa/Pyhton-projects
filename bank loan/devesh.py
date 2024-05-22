import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


 #this function will fix the names of columns and make simple names all in # smallcase with only _ as space and '-'

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

# remove_outliers will remove the outliers from a givem column in a fata frame

def ro(df,col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3-q1                   # inter quirtile range quater 3 minus quater 1
    lb = q1 - 1.5*iqr                 # lower bound
    ub = q3 + 1.5*iqr                     # upper bound
    return df.loc[(df[col]>lb)&(df[col]<ub)]

# histall function will make histogram of all the columns from the dataframe
def histall(df):
    cl = list(df.columns)
    ln = range(1,(len(cl)+1))
    l = zip(cl,ln)
    s=5
    plt.figure(figsize=(s,s*len(cl)))
    for i,j in l:
        plt.subplot(len(cl),1,j)
        plt.title( i)
        plt.xlabel('-'*100)
        sns.histplot(x=df[i])