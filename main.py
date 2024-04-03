import pandas as pd

from exploracion.exploracion_datos import *

df_def = pd.read_parquet("./clean/df_definitivo.parquet")

'''Ahora vamos a realizar un breve análisis exploratorio para visualizar mejor los datos y 
poder entender mejor el proceso de predicción de la siguiente práctica '''

#olasPorTiempo(df_def, 2023)

#distribuciones(df_def[['temp', 'dewPt', 'heat_index', 'rh','pressure', 'vis', 'wc', 'wspd', 'feels_like', 'uv_index',  'Vviento', 'AlturaOlas','PeriodoOlas', 'Temperatura', 'Lluvia', 'Nubosidad']])
#Ahora visualizamos todas las variables dummies juntas
#distribuciones_dummies(df_def[['wdir_E','wdir_ENE', 'wdir_ESE', 'wdir_N', 'wdir_NE', 'wdir_NNE', 'wdir_NNW', 'wdir_NW', 'wdir_S', 'wdir_SE', 'wdir_SSE', 'wdir_SSW', 'wdir_SW', 'wdir_VAR', 'wdir_W', 'wdir_WNW', 'wdir_WSW']])

#Correlaciones de columnas numéricas. Hemos eliminado todas las dummies procedentes de wdir_direction
#correlaciones(df_def[['temp', 'dewPt', 'heat_index', 'rh','pressure', 'vis', 'wc', 'wspd', 'feels_like', 'uv_index',  'Vviento', 'AlturaOlas','PeriodoOlas', 'Temperatura', 'Lluvia', 'Nubosidad']], 'spearman')

# medias y desviaciones de dummies
analisis_dummies(df_def, 'wdir_')

#Separamos en train y test
X_train, X_test, y_train, y_test = train_test_split(df_def.drop(columns=['AlturaOlas']), df_def.AlturaOlas, train_size=0.77)