from extraccion_datos import extraccion_datos_boya
from extraccion_datos import extraccion_datos_clima
from transformacion_datos import quitar_columnas_innecesarias
from transformacion_datos import tratar_na
from transformacion_datos import descomponerTiempo
from transformacion_datos import descomponerHoras
import json
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime


df_principal = extraccion_datos_boya()
df_secundario = extraccion_datos_clima("01/01/2022", "31/01/2022")
df_secundario = descomponerTiempo(df_secundario)

df_principal = tratar_na(df_principal)
df_secundario = quitar_columnas_innecesarias(df_secundario)
