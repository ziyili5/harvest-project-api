# curve fitting code
import numpy as np
from scipy.optimize import curve_fit  # we could import more, but this is what we need
from scipy.optimize import leastsq
from scipy.stats import pearsonr

"""
Fit the parameters of N-yield feild experiment data for one specific site in one year
:lin(x, y): linear fitting
:q(x,y): quandratic fitting
:qp(x,y): quandratic-plateau fitting
:param x: fertilizer rate experiment data
:param y: corresponding corn yield experiment data
"""


def lin(x, y):
    def Fun(p, x):  # define the fitting function
        a, b = p
        return a * x + b

    def error(p, x, y):  # fitting error
        return Fun(p, x) - y

    p0 = [0.519, 79.6]
    para = leastsq(error, p0, args=(x, y))
    return para[0]


def q(x, y):
    def Fq(p, x):
        a, b, c = p
        return a * x ** 2 + b * x + c

    def error(p, x, y):
        return Fq(p, x) - y

    p0 = [-0.002, 0.65, 80]
    para = leastsq(error, p0, args=(x, y))
    return para[0]


def qp(x, y):
    def Fqp(x, a, b, c):
        x0 = -1 * b / (2 * a)
        return np.piecewise(
            x,
            [x < x0, x >= x0],
            [lambda x: a * x * x + b * x + c, lambda x: (4 * a * c - b * b) / (4 * a)],
        )

    p0 = [-0.002, 0.65, 80]
    p, e = curve_fit(Fqp, x, y, p0)
    return p


def fit(x, y):
    p_lin = lin(x, y)
    y_lin = x * p_lin[0] + p_lin[1]
    cor_lin, _ = pearsonr(y, y_lin)

    p_q = q(x, y)
    y_q = p_q[0] * x ** 2 + p_q[1] * x + p_q[2]
    cor_q, _ = pearsonr(y, y_q)

    p_qp = qp(x, y)
    y_qp = [None] * len(x)
    for i in range(0, len(x)):
        if x[i] < (-1 * p_qp[1]) / (2 * p_qp[0]):
            y_qp[i] = p_qp[0] * x[i] ** 2 + p_qp[1] * x[i] + p_qp[2]
        else:
            y_qp[i] = (4 * p_qp[0] * p_qp[2] - p_qp[1] * p_qp[1]) / (4 * p_qp[0])
    cor_qp, _ = pearsonr(y, y_qp)

    if cor_lin > cor_q and cor_lin > cor_qp:
        Fit_type = "L"
        p = p_lin
    if cor_q > cor_lin and cor_q > cor_qp:
        Fit_type = "Q"
        p = p_q
    if cor_qp > cor_q and cor_qp > cor_lin:
        Fit_type = "QP"
        p = p_qp
    return Fit_type, p
