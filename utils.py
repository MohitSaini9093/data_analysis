# utils.py
from flask import session
import pandas as pd
import os

def get_dataframe():
    df_id = session.get('df_id')
    if not df_id:
        return None
    path = os.path.join('dataframes', f"{df_id}.pkl")
    print(path)
    if os.path.exists(path):
        return pd.read_pickle(path)
    return None