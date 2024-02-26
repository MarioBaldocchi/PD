import pandas as pd

def descomponerTiempo(df):
    """Descompone la columna valid_time_gmt en cuatro columnas nuevas: hora, dia, mes, anio. Elimina las columnas valid_time_gmt y expire_time_gmt"""
    df['hora'] = pd.to_datetime(df['valid_time_gmt'], unit='s').dt.hour
    df['dia'] = pd.to_datetime(df['valid_time_gmt'], unit='s').dt.day
    df['mes'] = pd.to_datetime(df['valid_time_gmt'], unit='s').dt.month
    df['anio'] = pd.to_datetime(df['valid_time_gmt'], unit='s').dt.year
    df.drop('valid_time_gmt', axis=1, inplace=True)
    df.drop('expire_time_gmt', axis=1, inplace=True)
    return df

def tratar_na(df):
    for col in df.columns:
        if df[col].isnull().all(): #Si la columna tiene todo nulos, la quitamos (no aporta información)
            df = df.drop(col, axis = 1)
        else:
            df[col] = df[col].fillna(0) #fixme Revisar cuando los dataframes esten unidos
    return df