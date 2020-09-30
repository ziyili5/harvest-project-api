import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def fig(tp, yn, cpr, fpr, En, Opy):
    """
    Draw the corresponding figures.
    See the following for more info in different figure types: http://cnrc.agron.iastate.edu/nRate.aspx
    :param tp: figure type:
                   1: Return to N
                   2: % of Max Yield
                   3: ENOR Frequency
                   4: ENOR vs. Yield
    :param yn:
    :param cpr:
    :param fpr:
    :param En:
    :param Opy:
    :return:
    """

    xn = np.linspace(0, 250, 1000)

    Yc = (yn.mean(axis=1) - yn.mean(axis=1)[0]) * cpr

    Yf = xn * fpr
    Yrtn = Yc - Yf

    A = np.where(Yrtn >= np.percentile(Yrtn, 98))
    Xmin = min(A[0])
    Xmax = max(A[0])

    if tp == 1:
        # Return to N
        plt.figure(figsize=(15, 10))
        plt.plot(xn, Yc, "b", label="Yield Return")
        plt.plot(xn, Yf, "g", label="Fertilizer Cost")
        plt.plot(xn, Yrtn, "r", label="Net Return")

        plt.fill_between(
            xn[A[0]],
            0,
            600,
            facecolor="cyan",
            alpha=0.3,
            label="Profitable N Rate Range(98%) "
            + str(round(xn[Xmin], 2))
            + "-"
            + str(round(xn[Xmax], 2)),
        )

        MRTN = xn[np.argmax(Yrtn, axis=0)]
        YRTN = max(Yrtn)
        plt.scatter(
            MRTN,
            YRTN,
            c="r",
            label="MRTN="
            + str(round(MRTN))
            + " Net Return to N at MRTN Rate="
            + str(round(YRTN, 2)),
        )

        plt.xlim(0, 250)
        plt.ylim(0, 600)
        plt.grid()
        plt.xlabel("Nitrogen rate(lb/acre)", fontsize=20)
        plt.ylabel("Benefits ($/acre)", fontsize=20)
        plt.tick_params(labelsize=15)

        plt.title("Return to N", fontsize=20)
        plt.legend(loc="upper left", fontsize=20)

    elif tp == 2:
        # % of Nax Yield
        plt.figure(figsize=(15, 10))

        Ypmy = yn.mean(axis=1) * 100 / max(yn.mean(axis=1))
        plt.plot(xn, Ypmy, "b", label="Yield Return")

        plt.fill_between(
            xn[A[0]],
            0,
            110,
            facecolor="cyan",
            alpha=0.3,
            label="Profitable N Rate Range(98%) "
            + str(round(xn[Xmin], 2))
            + "-"
            + str(round(xn[Xmax], 2)),
        )

        plt.xlim(0, 250)
        plt.ylim(0, 110)
        plt.grid()
        plt.tick_params(labelsize=15)
        plt.xlabel("Nitrogen rate(lb/acre)", fontsize=20)
        plt.ylabel("Percent of Maximum Yield", fontsize=20)
        plt.title("Return to N", fontsize=20)

    elif tp == 3:
        # frequency of ENOR distribution
        plt.figure(figsize=(15, 10))
        a = pd.cut(
            En,
            [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250],
            labels=[
                u"(0,25]",
                u"(25,50]",
                u"(50,75]",
                u"(75,100]",
                u"(100,125]",
                u"(125,150]",
                u"(150,175]",
                u"(175,200]",
                u"(200,225]",
                u"(225,250]",
            ],
        )
        b = a.value_counts()
        b2 = 100 * b / sum(b)
        b3 = b2.sort_index()
        c = {"section": b3.index, "frequency": b3.values}
        e = pd.DataFrame(c)

        sns.barplot(x="section", y="frequency", data=e, color="blue")  # palette设置颜色
        plt.grid()
        plt.tick_params(labelsize=15)
        # plt.xlim(0,250)
        plt.ylim(0, 40)
        plt.xlabel("Economic Optimum N Rate(lb/acre)", fontsize=20)
        plt.ylabel("% of Sitesd", fontsize=20)
        plt.title("Frequency of Economic Optium N Rate", fontsize=20)
        plt.tick_params(labelsize=15)

    elif tp == 4:
        # ENOR vs. Yield
        plt.figure(figsize=(15, 10))
        plt.scatter(En, Opy, s=40, c="blue")
        plt.xlim(0, 300)
        plt.ylim(0, 350)
        plt.grid()

        plt.xlabel("Optimum N Rate(lb/acre)", fontsize=20)
        plt.ylabel("Optimum Yield(bu/acre)", fontsize=20)
        plt.title("Relationship Between Economic Optimum N and Yield", fontsize=20)
        plt.tick_params(labelsize=15)

    plt.show()
