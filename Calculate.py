import pandas as pd
import numpy as np


def Cal(rot,fpr,cpr,dis):    
    xn=np.linspace(0,250,1000)
    df = pd.read_excel('/Users/aaronli/Documents/Others/MRTN_tool/Final_dis+region.xlsx', sheetname=rot+'_d'+str(dis))
    
    yn=np.zeros((1000,len(df)))
    #En=np.zeros((1,len(df)))
    #Opy=np.zeros((1,len(df)))

    En=[None]*len(df)
    Opy=[None]*len(df)
    for i in range(len(df)):
        C=df.iloc[i]['a']
        B=df.iloc[i]['b']
        A=df.iloc[i]['c']
        lx=df.iloc[i]['Model']
        MaxN=df.iloc[i]['MaxN']
        
        for j in range(len(xn)):
            if lx=='QP'or lx=='Q':#quandratic-plateau
                if B/(-2*A)<MaxN:
                    x0=B/(-2*A)
                else:
                    x0=MaxN
                if xn[j]<=x0:
                    yn[j,i]=A*xn[j]**2+B*xn[j]+C
                else:
                    yn[j,i]=A*x0**2+B*x0+C
            elif lx=='Q': #quandratic
                yn[j,i]=A*xn[j]**2+B*xn[j]+C
            else:#linear-plateau
                if xn[j]<=MaxN:
                    yn[j,i]=B*xn[j]+C
                else:
                    yn[j,i]=B*MaxN+C
        En[i]=xn[np.argmax(yn[:,i], axis=0)]
        Opy[i]=max(yn[:,i])
    return yn,En,Opy
