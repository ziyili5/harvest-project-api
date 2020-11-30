import numpy as np
import pandas as pd

def cal(rot, fpr, cpr, dis, fer):
    """
    Calculate the MRTN results and give input (fertilizer and corn price, rotation and district)
    :param rot: rotation - one of cc (continuous corn) and cs (corn-soybean rotation)
    :param fpr: nitrogen fertilizer price $/lb N
    :param cpr: corn price $/bu
    :param dis: district - a value from 1 to 13.
                1-9: districts 1-9
                10: northern
                11: lsw region
                12: central
                13: southern Illinois
    :param fer: fertilizer category
                1: Anhydrous Ammonia (82%)
                2: UAN (28%)
                3: UAN (32%)
                4: UAN (45%)
    :return:
    :yn: all N-yield responses curve under selected districts and rotations
             (each column represent one N-yield response for one site in one year)
    :En: Economic optimum N rates (EONR) under selected districts and rotations
         (each value represents one EONR for one site in one year)
    :Opy: all optimal yields under selected districts and rotations
          (each value represent one optimal yield for one site in one year)
    :MRTN_rate: the final recommendation N fertilizer rate (MRTN) at the selected district
    :Ns: sites number of the selected districts
    :NRN: Net return to N at MRTN Rate
    :PMY: % of Maximum Yield at MRTN Rate
    :Rg_min and Rg_max: Profitable N Rate Range
    :FM: Fertilizer at MRTN Rate
    :FC: Fertilizer Cost at MRTN Rate
    """
    xn = np.linspace(0, 300, 1000)
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
            if lx == "QP":  # quandratic-plateau
                x0 = B / (-2 * A)
                if x0>=MaxN:
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

    Yc = (yn.mean(axis=1) - yn.mean(axis=1)[0]) * cpr  # Crop benefits
    Yf = xn * fpr  # Fertilizer cost
    Yrtn = Yc - Yf  # Return to N

    Ns = yn.shape[1]  # number of sites
    MRTN_rate = xn[np.argmax(Yrtn, axis=0)]  # MRTN rate

    YN=yn.mean(axis=1)
    Y_mrtn=YN[np.argmax(Yrtn, axis=0)]#Crop yield at MRTN rate
    PMY=Y_mrtn/max(YN) # % of Maximum Yield at MRTN Rate

    NRN = Yrtn[np.argmax(Yrtn, axis=0)]  # Net return to N at MRTN Rate
    Rg_min = min(xn[np.where(Yrtn >= NRN - 1)])  # Profitable N rate range
    Rg_max = max(xn[np.where(Yrtn >= NRN - 1)])  # Profitable N rate range


    if fer == "Anhydrous Ammonia (82%)":
        nt = 0.82
    elif fer == 1:
        nt = 0.28
    elif fer == 2:
        nt = 0.32
    elif fer == 3:
        nt = 0.45
    else:
        nt = 0.21
    FM = MRTN_rate / nt  # Fertilizer amount at MRTN Rate
    FC = Yf[np.argmax(Yrtn, axis=0)]  # Fertilizer cost at MRTN Rate

    return yn, En, Opy, MRTN_rate, Ns, NRN, PMY, Rg_min, Rg_max, FM, FC
