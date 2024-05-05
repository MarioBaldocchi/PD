# #### Archivo de preprocesamiento de datos meteorologicos (fuente secundaria)


# Importamos librerías necesarias
import pandas as pd
from datetime import datetime, timezone
import os

def descomponer_fecha(df):
    df['fecha'] = pd.to_datetime(df['validTimeUtc'], utc=True)
    df['hora'] = df['fecha'].dt.hour
    df['dia'] = df['fecha'].dt.day
    df['mes'] = df['fecha'].dt.month
    df['anio'] = df['fecha'].dt.year
    df.drop('validTimeUtc', axis=1, inplace=True)
    return df

def obtener_columnas_relevantes(df):
    df = df.rename(columns={'temperature': 'temp', 
                            'temperatureDewPoint': 'dewPt', 
                            'temperatureHeatIndex':'heat_index', 
                            'relativeHumidity':'rh', 
                            'pressureMeanSeaLevel':'pressure', 
                            'visibility':'vis', 
                            'temperatureWindChill':'wc', 
                            'temperatureFeelsLike':'feels_like',
                            'uvIndex':'uv_index'})
    df = df[['hora', 'dia', 'mes', 'anio', 'temp', 'dewPt', 'heat_index', 'rh', 'pressure', 'vis', 'wc', 'feels_like', 'uv_index', 'windDirectionCardinal']]
    return df

def preprocess(data, fecha_pred):
    data = descomponer_fecha(data)
    data['antelacion'] = (pd.to_datetime(data['fecha']) - fecha_pred).dt.total_seconds() // 3600
    data = obtener_columnas_relevantes(data)
    return data

dfs = []
dirName = '../secundaria-raw'
directory = os.fsencode(dirName)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
        df = preprocess(pd.read_json(dirName + "/" + filename), datetime.strptime(filename.replace('h', ''), '%H_%d_%m_%Y.json').replace(tzinfo=timezone.utc))
        dfs.append(df)


# Creamos directorio de salida si no existe
outDir = '../clean'
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Guardamos el dataframe concatenando todos los archivos en uno
pd.concat(dfs).to_csv(outDir+'/forecast_meteo.csv', index=False)


