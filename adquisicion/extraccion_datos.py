import pandas as pd
import requests
import datetime

from extraccion_drive import procesar_archivo_info
from extraccion_drive import descargar_archivo_directo
from pathlib import Path


def subtract30Days(date):
    """Resta a la fecha pasada un intervalo de 30 días"""
    return date - datetime.timedelta(days=30)

def extraccion_datos():
    """Devuelve dos dataFrames: el de la fuente principal y el de la fuente secundaria"""
    path = Path.cwd()
    lista_links_archivos = procesar_archivo_info(Path(path, "archivos_info.txt"))
    rutas_archivos = []

    for link_archivo in lista_links_archivos:
        _, ruta_completa = descargar_archivo_directo(link_archivo[0], link_archivo[2], link_archivo[1])
        rutas_archivos.append(ruta_completa)
    #df_principal = pd.read_parquet(rutas_archivos[0])
    #df_secundario = pd.read_parquet(rutas_archivos[1])

    #return df_principal, df_secundario

def extraccion_datos_clima(ini, fin):
  """Dado un periodo máximo de 31 días, devuelve los datos climatológicos (por hora) de cada día"""
    # ini y fin en formato datetime lo pasamos a int
  fechaIni = int(ini.strftime("%Y%m%d"))
  fechaFin = int(fin.strftime("%Y%m%d"))

  datos = {
    "apiKey": "e1f10a1e78da46f5b10a1e78da96f525",
    "units": "e",
    "startDate": fechaIni,
    "endDate": fechaFin
  }
  tablaWeather = requests.get("https://api.weather.com/v1/location/EIWF:9:IE/observations/historical.json", params=datos).json()
  df = pd.DataFrame.from_dict(tablaWeather["observations"])
  return df

def extraccion_df_secundario(fechaIni, fechaFin):
    """fechaIni y fechaFin son gechas en formato datetime de python"""
    result = None

    fechaSup = fechaFin
    fechaInf = subtract30Days(fechaSup)
    while(fechaIni < fechaSup):
        if (fechaIni > fechaInf):
            # si se pasa del limite inferior, subirlo al limite
            fechaInf = fechaIni

        if result is None:
            result = extraccion_datos_clima(fechaInf, fechaSup)
        else:
            result = pd.concat([result, extraccion_datos_clima(fechaInf, fechaSup)])
        # siguiente intervalo de 30 dias
        fechaSup = fechaInf
        fechaInf = subtract30Days(fechaSup)

    return result
