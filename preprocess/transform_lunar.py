import pandas as pd


def preprocess_lunar(df):
    df = df[["datetime", "moonphase"]]
    df[['anio', 'mes', 'dia']] = df['datetime'].str.split('-', expand=True)
    df = df.drop(columns=["datetime"])

    df['anio'] = df["anio"].astype(int)
    df['mes'] = df["mes"].astype(int)
    df['dia'] = df["dia"].astype(int)
    moonphase = df.pop("moonphase")
    df["moonphase"] = moonphase

    return df
