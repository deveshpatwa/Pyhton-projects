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


