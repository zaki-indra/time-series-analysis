from time import sleep
import pandas as pd
import numpy as np
import keras

from datetime import timedelta
import msvcrt

'''
project structure:

project-directory/
|- program.py (this)
|- models/
    |- my_model_<num>.h5
|- data/
    |- train.csv
'''

DATA_PATH = "data/train.csv"
MODEL_PATH = "models/my_model_3.h5"

def fourier_transform(dataframe:pd.DataFrame) -> pd.DataFrame:
    temp = dataframe.copy()
    date_time = pd.to_datetime(temp.pop("date"), format='%Y-%m-%d')

    day = 24*60*60
    year = (365.2425)*day
    
    timestamp_s = date_time.map(pd.Timestamp.timestamp)
    
    temp['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    temp['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
    temp = temp.set_index(date_time)
    return temp

def run():
    reference = pd.read_csv(DATA_PATH)
    reference = fourier_transform(reference)

    model = keras.models.load_model(MODEL_PATH)
    model.summary()

    ask(reference, model)
    
def ask(reference:pd.DataFrame, model:keras.Model):
    data = reference.copy()
    while True:
        print("PRESS ENTER TO CONTINUE:")
        sleep(0.5)
        inp = msvcrt.getch()
        if inp.lower() != b"\r":
            exit(0)

        date = input("Date (format: %YYYY-%mm-%dd): ")
        store = int(input("Store: "))
        item = int(input("Item: "))
        date = pd.to_datetime(date, format='%Y-%m-%d')
        
        process(data, reference, model, date, store, item)
        
def process(data:pd.DataFrame, reference:pd.DataFrame, model:keras.Model, date, store, item):
    temp = data[(data["store"] == store) & (data["item"] == item)].copy()
    try:
        sales = temp.loc[date, "sales"]
        print("Actual sales:", sales)
    except KeyError:
        print("Actual sales: ??")
    predict(reference, model, date, store, item)

def predict(reference:pd.DataFrame, model:keras.Model, date, store, item):
    temp_ref = reference[(reference["store"] == store) & (reference["item"] == item)].copy()
    _30day_before = date - timedelta(days=30)
    _day_before = date - timedelta(days=1)
    first_day = pd.to_datetime("2013-01-01", format='%Y-%m-%d')

    if _30day_before < first_day:
        print("Date must > 2013-02-01")

    try:
        sales = temp_ref.loc[_day_before, "sales"]
    except KeyError:
        find_val(reference, model, _day_before, store, item)

    temp_ref = reference[(reference["store"] == store) & (reference["item"] == item)].copy()
    temp_ref:pd.DataFrame = temp_ref.loc[_30day_before:_day_before, ["sales", "Year sin", "Year cos"]]

    y_pred = model.predict([np.array([[store, item]]), temp_ref.to_numpy().reshape((-1, 30, 3))])
    y_rounded = int(np.round(y_pred)[0, 0])
    print("Predicted sales:", y_rounded)


def find_val(reference:pd.DataFrame, model:keras.Model, date, store, item):
    temp_ref = reference[(reference["store"] == store) & (reference["item"] == item)].copy()
    _30day_before = date - timedelta(days=30)
    _day_before = date - timedelta(days=1)

    try:
        sales = temp_ref.loc[_day_before, "sales"]
    except KeyError:
        find_val(reference, model, _day_before, store, item)

    temp_ref = reference[(reference["store"] == store) & (reference["item"] == item)].copy()
    temp_ref:pd.DataFrame = temp_ref.loc[_30day_before:_day_before, ["sales", "Year sin", "Year cos"]]

    y_pred = model.predict([np.array([[store, item]]), temp_ref.to_numpy().reshape((-1, 30, 3))])
    y_rounded = int(np.round(y_pred)[0, 0])

    day = 24*60*60
    year = (365.2425)*day
    
    timestamp_s = pd.Timestamp.timestamp(date)
    
    year_sin = np.sin(timestamp_s * (2 * np.pi / year))
    year_cos = np.cos(timestamp_s * (2 * np.pi / year))
    reference.loc[date] = [store, item, y_rounded, year_sin, year_cos]

if __name__ == "__main__":
    run()