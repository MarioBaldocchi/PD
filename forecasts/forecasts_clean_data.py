import os

import pandas as pd

'''
Depende de la ruta donde se ejecuta el .py

from forecasts.capturar_altura_olas import caturar_altura_olas
from forecasts.preprocess.preprocess_forecast_boya import forecast_boya_clean
from forecasts.preprocess.preprocess_forecast_luna import forecast_lunar_clean
from forecasts.preprocess.preprocess_forecast_meteo import forecast_meteo_clean
'''

#Si se ejecuta desde PD> o PD\forecasts>
from capturar_altura_olas import caturar_altura_olas
from preprocess.preprocess_forecast_boya import forecast_boya_clean
from preprocess.preprocess_forecast_luna import forecast_lunar_clean
from preprocess.preprocess_forecast_meteo import forecast_meteo_clean


def cambiar_tipo(tipo, columnas, df):
    """Dado un dataframe, unas columnas y un tipo, covierte el tipo de las columnas al tipo especificado"""
    for col in columnas:
        df[col] = df[col].astype(tipo)
    return df

# Devuelve la unión de las predicciones de diferentes fuente limpio
def forecasts_clean_merged():

    #df_boya = pd.read_csv('./clean/forecast_boya.csv')  # primaria
    #df_meteo = pd.read_csv('./clean/forecast_meteo.csv')  # secundaria
    #df_luna = pd.read_csv('./clean/forecast_luna.csv')  # terciaria

    df_boya = forecast_boya_clean()  # primaria
    df_meteo = forecast_meteo_clean()  # secundaria
    df_luna = forecast_lunar_clean()  # terciaria

    df_def = df_boya.merge(df_meteo, on=['anio', 'mes', 'dia', 'hora', 'antelacion'])
    df_def = df_def.merge(df_luna, on=['anio', 'mes', 'dia'])
    # vemos que algunas columnas no tienen el tipo correcto
    df_def = cambiar_tipo('int', ['Vviento', 'PeriodoOlas', 'Temperatura', 'Nubosidad'], df_def)
    df_def = cambiar_tipo('float', ['Lluvia'], df_def)

    df_def.drop(columns='Temperatura', inplace=True) # sale duplicada, la eliminamos

    # Para la respuesta sacamos datos de las observaciones (valores reales)
    # ordenamos para poder sacar el primer y el ultimo dia
    df_def = df_def.sort_values(['anio', 'mes', 'dia'], ascending=[True, True, True])
    first_day = df_def.iloc[0]
    last_day = df_def.iloc[-1]

    # left join, si no ha llegado el día, le asignamos NA a la altura de la ola
    df_def = df_def.merge(caturar_altura_olas(first_day, last_day), how='left', on=['anio', 'mes', 'dia', 'hora'])

    return df_def

outDir = 'clean'
if not os.path.exists(outDir):
    os.makedirs(outDir)
forecasts_clean_merged().to_csv(outDir + '/forecast_merged.csv', index=False)