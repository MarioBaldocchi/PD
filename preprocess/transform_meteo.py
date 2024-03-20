"""
Archivo preprocesar el dataframe de datos meteorológicos(df_secundario)
"""

import pandas as pd
from transform_general import *
from agregacion_hora import *
def preprocess_meteo(df):
    # Movemos la fecha del indice a la columna fecha y la transformamos en formato datetime pandas
    df = descomponerTiempoUnix(df).sort_values(['anio', 'mes', 'dia'], ascending=[True, True, True])
    """TRANSFORMACIÓN DE LOS DATOS"""
    # Quitamos las columnas que solo tomen un valor (no aportan información relevante para las predicciones)
    df = quitar_columnas_innecesarias(df)
    # Columnas descartadas manualmente
    df = quitar_columnas_manual(df)
    # Convertimos wdir a variables dummy
    df = preprocess_wdir(df)

    # Agregamos los datos por cada hora (nos quedamos con 1 fila para cada hora)
    df = aggregate_secondary(df, ['anio', 'mes', 'dia', 'hora'])

    # Quitando las columnas anteriormente mencionadas, nos quedan 17 observaciones (filas) con algún na en df_secundario. La mayoría (15) se dan el 1
    # de Febrero de 2022 debido a un error del aparato que calcula el uv_index (yo optaría por quitar las observaciones del 1
    # de Febrero en df_principal y df_secundario. Las otras dos filas con na también las quitaría, porque son de horas distintas
    # (al tener 2 observaciones seguríamos teniendo observaciones para todas las horas)
    df.dropna(inplace=True)  # Quitamos las filas con algún na

    return df

def descomponerTiempoUnix(df):
    """Descompone la columna valid_time_gmt en cuatro columnas nuevas: hora, dia, mes, anio. Elimina las columnas valid_time_gmt y expire_time_gmt"""
    df_tmp = df.copy()
    df_tmp['hora'] = pd.to_datetime(df['valid_time_gmt'], unit='s').dt.hour
    df_tmp['dia'] = pd.to_datetime(df['valid_time_gmt'], unit='s').dt.day
    df_tmp['mes'] = pd.to_datetime(df['valid_time_gmt'], unit='s').dt.month
    df_tmp['anio'] = pd.to_datetime(df['valid_time_gmt'], unit='s').dt.year
    df_tmp.drop('valid_time_gmt', axis=1, inplace=True)
    df_tmp.drop('expire_time_gmt', axis=1, inplace=True)

    return df_tmp

def quitar_columnas_manual(df):
    """Eliminamos columnas del df:
            gust: muchos nan (es preferible quitar la variable antes que eliminar muchas observaciones)
            wdir: muchos nan (es preferible quitar la variable antes que eliminar muchas observaciones). PD: la eliminación de la columna wdir no nos afecta porque podemos obtener dicha información
                                                                                                             a partir de la columna wdir_cardinal, la cual en vez de ser numérica es categórica
            day_ind: nos dice si es de noche(N) o de dia(D), lo podemos saber con la hora actual
            wx_icon: icono que se usó para la visualización(nube, lluvia)
            icon_extd: parecida a wx_icon
            clds: nivel de nubosidad, ya esta especidicada con numeros en la fuente principal.
            wx_phrase: Frase para describir el tiempo. Se calcula a partir de otras columnas.
            uv_desc: Descripcion del estado de ultravioleta. Se saca a aprtir de uv_index. 0-2 Low, 3-5 Moderate, 6-7 High
            """
    df.drop(columns=["day_ind", "wx_icon", "icon_extd", "gust", "wdir", "clds", "wx_phrase", "uv_desc"],
            inplace=True)
    return df


def preprocess_wdir(df):
    # Convertimos la columnas dirección de viento a variables dummy
    # Reemplazamos por NA los datos de wdir_cardinal == CALM para asi no salga en las variables dummy
    df.loc[df['wdir_cardinal'] == 'CALM', 'wdir_cardinal'] = pd.NA

    df = pd.get_dummies(df, prefix='wdir', columns=['wdir_cardinal'], dtype='int')

    return df