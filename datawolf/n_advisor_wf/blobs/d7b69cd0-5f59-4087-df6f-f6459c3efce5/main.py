import json

import click
from calculate import cal
from figure import fig
from figure import get_plot_data


@click.command()
@click.option(
    "--rot",
    required=True,
    type=str,
    help="rotation cc:continuous corn; cs:corn-soybean rotation",
)
@click.option(
    "--fpr", required=True, type=float, help="nitrogen fertilizer price $/lb N"
)
@click.option("--cpr", required=True, type=float, help="corn price $/bu")
@click.option(
    "--dis",
    required=True,
    type=int,
    help="""
        district:\n
        \t1-9: districts 1-9\n
        \t10-13 northern, lsw region, central, and southern Illinois
        """,
)
@click.option(
    "--fer",
    required=True,
    type=int,
    help="""
        Fertilizer category:\n
        \t1: Anhydrous Ammonia (82%)\n
        \t2: UAN (28%)\n
        \t3: UAN (32%)\n
        \t4: UAN (45%)
        """,
)
@click.option("--output", default="std", help="std, json, plot")
@click.option("--filename", default="", help="The filename for json output")
@click.option(
    "--plot",
    default=1,
    help="""
        figure type:\n
        \t0: No plot\n
        \t1: Return to N\n
        \t2: % of Max Yield\n
        \t3: ENOR Frequency\n
        \t4: ENOR vs. Yield
        """,
)
def run(rot, fpr, cpr, dis, plot, fer, output, filename):
    (yn, En, Opy, MRTN_rate, Ns, NRN, PMY, Rg_min, Rg_max, FM, FC) = cal(
        rot, fpr, cpr, dis, fer
    )
    if output == "std":
        print(yn, En, Opy, MRTN_rate, Ns)
    elif output == "json":
        (xn, Yc, Yf, Yrtn, Ypmy, A, Xmin, Xmax) = get_plot_data(yn, fpr, cpr)
        results = json.dumps(
            {
                "yn": yn.tolist(),
                "En": En,
                "Opy": Opy,
                "MRTN_rate": MRTN_rate,
                "Ns": Ns,
                "xn": xn.tolist(),
                "Yc": Yc.tolist(),
                "Yf": Yf.tolist(),
                "Yrtn": Yrtn.tolist(),
                "Ypmy": Ypmy.tolist(),
                "A": A[0].tolist(),
                "Xmin": Xmin.tolist(),
                "Xmax": Xmax.tolist(),
            }
        )
        if filename:
            with open(filename, "w") as f:
                f.write(results)
        else:
            print(results, flush=True)
    elif output == "plot":
        fig(plot, yn, En, Opy, cpr, fpr, Rg_min, Rg_max)


if __name__ == "__main__":
    run()
