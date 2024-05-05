# #### Archivo de preprocesamiento de datos de la boya (fuente principal)
import numpy as np
# Importamos librerías necesarias

import pandas as pd
from datetime import datetime
import os

'''
 Esta función se encarga de averiguar para que fecha se predice a partir de la fecha
 en la que se consulto, la hora y el dia. La devuelve en formateo datetime para calcular facilmente
 la antelacion posteriormente
 '''
def sacar_fecha_target(valor, fecha_pred):    
    # sacamos dia y hora del valor
    hora = int(valor[-3:-1])
    dia = int(valor[2:-4])

    fecha = fecha_pred
    fecha = fecha.replace(hour=hora, day=dia)
    if (dia < fecha_pred.day):
        # estan en meses o anios diferentes, ej 31 -> 1
        if (fecha_pred.month == 12): # si es diciembre -> cambiamos de anio
            fecha.replace(month=1, year=fecha_pred.year + 1)
        else:
            fecha.replace(month=fecha_pred.month + 1)

    return fecha        


'''
Esta funcion realiza el preprocesado(renombra columnas, calcula antelacion y elimina filas pasadas)
'''
def preprocess_df(df, fecha_pred):
    # transponemos la matriz
    df = df.T
    df.columns = ['Vviento', 'AlturaOlas', 'PeriodoOlas', 'Temperatura', 'Nubosidad', 'Lluvia']

    # Con estos valores se asignan ceros en la variable Lluvia
    df.replace('\xa0', 0, inplace=True)
    df['fecha'] = df.index.map(lambda x: sacar_fecha_target(x, fecha_pred))
    # nos quedamos con predicciones (descartamos pasado)
    df = df[df['fecha'] >= fecha_pred]
    # calculamos antelacion (en horas)
    df['antelacion'] = ((pd.to_datetime(df['fecha']) - fecha_pred).dt.total_seconds() // 3600).astype('int')
    df['hora'] = df.fecha.dt.hour
    df['dia'] = df.fecha.dt.day
    df['anio'] = df.fecha.dt.year
    df['mes'] = df.fecha.dt.month

    df = df.drop(columns=['fecha', 'AlturaOlas'])
    df = df.reset_index(drop=True)
    # no hay na's al ser predicciones
    #df = df.fillna(0)
    #df = df[~df.map(lambda x: x == '-').any(axis=1)]
    return df


# Los archivos tienen datos de predicciones. Además por alguna razón se mezclan con datos reales(sigue apareciendo una hora, cuando ya ha pasado)
# 
# Asumimos que el formato del archivo es 10h_03_05_2024.csv, donde:
# - 10 - hora
# - 03 - dia
# - 05 - mes
# - 2024 - anio

dirName = '../boya-raw'
directory = os.fsencode(dirName)
dfs = []
# recorremos todos los datos sacados y los guardamos de forma preprocesada
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        # sacamos los datos de fecha en la que se guardaron las predicciones
        # para poder calcular con cuanta antelación (en horas) se hizo la predicción
        fecha = datetime.strptime(filename.replace('h', ''), '%H_%d_%m_%Y.csv')
        df = pd.read_csv(dirName + "/" + filename)
        df = preprocess_df(df, fecha)
        #df['filename'] = filename
        dfs.append(df)


# Creamos directorio de salida si no existe
outDir = '../clean'
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Guardamos el dataframe concatenando todos los archivos en uno

# juntamos los df's y los guardamos
pd.concat(dfs).to_csv(outDir+'/forecast_boya.csv', index=False)

