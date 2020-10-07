import numpy as np
import pandas as pd


def cal(rot, fpr, cpr, dis):
    """
    Calculate the MRTN results and give input (fertilizer and corn price, rotation and district)
    :param rot: rotation -  one of cc (continuous corn) and cs (corn-soybean rotation)
    :param fpr: nitrogen fertilizer price $/lb N
    :param cpr: corn price $/bu
    :param dis: district - a value from 1 to 13.
                1-9: districts 1-9
                10: northern
                11: lsw region
                12: central
                13: southern Illinois
    """
    xn = np.linspace(0, 250, 1000)
    df = pd.read_excel("./data/Final_dis+region.xlsx", sheet_name=f"{rot}_d{dis}",)

    yn = np.zeros((1000, len(df)))
    # En=np.zeros((1,len(df)))
    # Opy=np.zeros((1,len(df)))

    En = [None] * len(df)
    Opy = [None] * len(df)
    for i in range(len(df)):
        C = df.iloc[i]["a"]
        B = df.iloc[i]["b"]
        A = df.iloc[i]["c"]
        lx = df.iloc[i]["Model"]
        MaxN = df.iloc[i]["MaxN"]

        for j in range(len(xn)):
            if lx == "QP" or lx == "Q":  # quandratic-plateau
                if B / (-2 * A) < MaxN:
                    x0 = B / (-2 * A)
                else:
                    x0 = MaxN
                if xn[j] <= x0:
                    yn[j, i] = A * xn[j] ** 2 + B * xn[j] + C
                else:
                    yn[j, i] = A * x0 ** 2 + B * x0 + C
            elif lx == "Q":  # quandratic
                yn[j, i] = A * xn[j] ** 2 + B * xn[j] + C
            else:  # linear-plateau
                if xn[j] <= MaxN:
                    yn[j, i] = B * xn[j] + C
                else:
                    yn[j, i] = B * MaxN + C
        En[i] = xn[np.argmax(yn[:, i], axis=0)]
        Opy[i] = max(yn[:, i])
    return yn, En, Opy
    """
    Return values for cal() funcrion
    :yn: all N-yield responses curve under selected districts and rotations(each column represent one N-yield response for one site in one year)
    :En: recommended Econominc optimum N rate (one value) in under selected districts and rotations
    :Opy: all optimal yields under selected districts and rotations (each value represent one optimal yield for one site in one year)
    """
