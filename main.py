from extraccion_datos import *
from transformacion_datos import quitar_columnas_innecesarias
from transformacion_datos import tratar_na
from transformacion_datos import descomponerTiempo
from utils import *


df_principal = extraccion_datos_boya()


df_secundario = extraccion_df_secundario(stringToDatetime("01/01/2022"), stringToDatetime("31/12/2023"))
df_secundario = descomponerTiempo(df_secundario)
print(df_secundario)
df_principal = tratar_na(df_principal)
df_secundario = quitar_columnas_innecesarias(df_secundario)
