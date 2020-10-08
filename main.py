import json

import click

from calculate import cal
from figure import fig


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
@click.option("--output", default="std", help="std, json, plot")
@click.option("--filename", default="results.json", help="The filename for json output")
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
def run(rot, fpr, cpr, dis, plot, output, filename):
    (yn, En, Opy, MRTN_rate, Ns) = cal(rot, fpr, cpr, dis)
    if output == "std":
        print(yn, En, Opy, MRTN_rate, Ns)
    elif output == "json":
        with open(filename, "w") as f:
            f.write(
                json.dumps(
                    {
                        "yn": yn.tolist(),
                        "En": En,
                        "Opy": Opy,
                        "MRTN_rate": MRTN_rate,
                        "Ns": Ns,
                    }
                )
            )
    elif output == "plot":
        fig(plot, yn, En, Opy, cpr, fpr)


if __name__ == "__main__":
    run()
