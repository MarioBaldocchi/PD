# #### Archivo de preprocesamiento de datos de fase lunar (fuente terciaria)

# Importamos librerías necesarias
import pandas as pd
import os

def preprocess_lunar(df):
    df = df[["datetime", "moonphase"]]
    df['dia'] = df.datetime.dt.day.astype(int)
    df['mes'] = df.datetime.dt.month.astype(int)
    df['anio'] = df.datetime.dt.year.astype(int)
    df = df.drop(columns=["datetime"])
    return df

dfs = []
dirName = '../terciaria-raw'
directory = os.fsencode(dirName)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
        df = preprocess_lunar(pd.read_json(dirName + "/" + filename))
        dfs.append(df)


# Creamos directorio de salida si no existe
outDir = '../clean'
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Guardamos el dataframe concatenando todos los archivos en uno
df = pd.concat(dfs)
# por si se repiten filas
df.drop_duplicates(inplace=True)

df.to_csv(outDir+'/forecast_luna.csv', index=False)


