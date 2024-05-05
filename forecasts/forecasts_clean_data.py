import pandas as pd

def cambiar_tipo(tipo, columnas, df):
    """Dado un dataframe, unas columnas y un tipo, covierte el tipo de las columnas al tipo especificado"""
    for col in columnas:
        df[col] = df[col].astype(tipo)
    return df

# Devuelve la unión de las predicciones de diferentes fuente limpio
def forecasts_clean_merged():
    df_boya = pd.read_csv('./clean/forecast_boya.csv')  # primaria
    df_meteo = pd.read_csv('./clean/forecast_meteo.csv')  # secundaria
    df_luna = pd.read_csv('./clean/forecast_luna.csv')  # terciaria
    df_def = df_boya.merge(df_meteo, on=['anio', 'mes', 'dia', 'hora', 'antelacion'])
    df_def = df_def.merge(df_luna, on=['anio', 'mes', 'dia']).sort_values(['anio', 'mes', 'dia'], ascending=[True, True, True])
    # vemos que algunas columnas no tienen el tipo correcto
    df_def = cambiar_tipo('int', ['Vviento', 'PeriodoOlas', 'Temperatura', 'Nubosidad'], df_def)
    df_def = cambiar_tipo('float', ['AlturaOlas', 'Lluvia'], df_def)

    df_def.drop(columns='Temperatura', inplace=True) # sale duplicada, la eliminamos

    return df_def


forecasts_clean_merged().to_csv('./clean/forecast_merged.csv', index=False)