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

## About the return values

This part is related to the final results display in the websites

- 'MRTN Rate' is the N rate at the MRTN(finally recommended N rate). For the data set, rotation, and price ratio(s), the MRTN rate would be the suggested rate to apply for maximizing net return to N application.
- 'Return to N' is the economic net return (EONR) at the MRTN rate.
- '% of Max Yield' is the proportion of yield that might be produced at the MRTN rate compared to the yield at the maximum response to N
- 'EONR Frequency' is the frequency distribution, in 25 lb N increments, of the EONR for each site in the dataset and rotation chosen.
- 'EONR vs. Yield' is the relationship between the site EONR and yield at the EONR for each site in the dataset and rotation chosen.
