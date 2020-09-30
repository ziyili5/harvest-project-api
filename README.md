# N_recom

This is the code for building N recommendation website.

- `curve_fit.py` is used to fit the field-experiment N-yield response data and get the fitted parameters.
- `calculate.py` is used to calculate the recommended N in one specific region given the rotation (corn-soybean and corn-corn) method and corn & fertilizer price.
- `figure.py` is used to visualize the final N recommendation.
- `main.py` is the main function, you can run the main function to get the corresponding N recommendation result for an specific region.

## How to use

> Requires python 3

- Install the dependencies by running `pip install -r requirements.txt`.
- If you are going to contribute code, install the dev dependencies (`pip install -r requirements-dev.txt`)
  and then run `pre-commit install`.
- Run `python main.py --help` to see a list of arguments for the cli.
