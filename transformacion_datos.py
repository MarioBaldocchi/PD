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


def descomponerHoras(df):
    """Transforma columnas con los datos horarios a filas con columna hora"""
    new_df = None # dataframe separados por horas

    for h in range(0, 24):
        hora = str(h).zfill(2) # necesitamos horas de dos digitos
        separate_df = columnasAFilas(df, hora)
        if new_df is None:
            new_df = separate_df
        else:
            new_df = pd.concat([new_df, separate_df]) # unimos con el dataframe anterior

    return new_df


def columnasAFilas(df, hora):
    "Saca los datos para una hora concreta(columnas que acaban por esa hora)"
    selected_cols = df.columns[df.columns.str.endswith(hora)] # columnas que acaban en esa hora
    # Sacamos las columnas de la hora actual
    separate_df = df.loc[:][selected_cols]
    # Renombramos las columnas (quitamos hora del fin)
    cols_sin_hora = selected_cols.str.slice(stop=-2)
    separate_df = separate_df.rename(dict(zip(separate_df.columns, cols_sin_hora)), axis=1)
    separate_df["hora"] = hora

    return separate_df