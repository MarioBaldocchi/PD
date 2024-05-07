"""
Archivo para preprocesar los datos de boya(df_principal)
"""

import pandas as pd
from transform_utils import *

def preprocess_boya(df):
    df.reset_index(inplace=True)
    df.rename(columns={"index": 'fecha'}, inplace=True)
    df.fecha = pd.to_datetime(df.fecha, format='%d.%m.%Y')
    #df = quitar_columnas_innecesarias(df)
    # Los na representan 0's, por lo que los tratamos
    df = tratar_na(df)
    # En cambio los guiones representan datos no evaluados. Por tanto tenemos que eliminar las filas que contengan guiones
    df = df[~df.map(lambda x: x == '-').any(axis=1)]
    # Para tener las horas como filas, no como columnas
    df = descomponerHoras(df)

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
    separate_df["hora"] = int(hora) # pasamos hora a numero
    # para no perder la fecha
    separate_df['dia'] = df.fecha.dt.day
    separate_df['mes'] = df.fecha.dt.month
    separate_df['anio'] = df.fecha.dt.year
    return separate_df