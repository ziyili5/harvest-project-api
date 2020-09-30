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
@click.option(
    "--plot",
    default=0,
    help="""
        figure type:\n
        \t0: No plot\n
        \t1: Return to N\n
        \t2: % of Max Yield\n
        \t3: ENOR Frequency\n
        \t4: ENOR vs. Yield
        """,
)
def run(rot, fpr, cpr, dis, plot):
    (yn, En, Opy) = cal(rot, fpr, cpr, dis)
    print(yn, En, Opy)
    if plot:
        fig(plot, yn, cpr, fpr, En, Opy)


if __name__ == "__main__":
    run()
