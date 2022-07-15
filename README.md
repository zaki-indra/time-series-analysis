# Time Series Analysis
Predicting sales of an item inside a store
dataset: https://drive.google.com/uc?id=1RQEXXW3aW2LHAawFo0OiAXfYWYgwF0Gh

## How to make predictions using the model
1. Train the model in `training.ipynb`.
2. Run the `program.py` file from the terminal.
> `$ python program.py`
3. Enter corresponding date, store, and item for prediction. for example:
> `Date (format: %YYYY-%mm-%dd): 2019-01-01`<br>
> `Store: 1`<br>
> `Item: 6`
4. See results.
> if date is in dataset:
>> `Actual sales: 9`<br> `Predicted sales: 14`


> if date isn't in dataset:
>> `Actual sales: ??`<br>`Predicted sales: 45`
