import pandas as pd
import requests
from utils import subtract30Days

from extraccion_drive import procesar_archivo_info
from extraccion_drive import descargar_archivo_directo
def extraccion_datos_boya():

    """Devuelve un dataFrame con los datos obtenidos de la boya localizada en la playa de Tramore"""

    """Solo vamos a tener un archivo a descargar desde el drive, por lo que nuestra lista es 
        de 1 solo elemento"""
    tuplas_links = procesar_archivo_info("./archivos_info.txt")
    tupla_link = tuplas_links[0]
    archivo_destino, ruta_completa = descargar_archivo_directo(tupla_link[0],tupla_link[2], tupla_link[1])
    df = pd.read_csv(ruta_completa, sep = ";", index_col=[0])
    return df

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

        if (result is None):
            result = extraccion_datos_clima(fechaInf, fechaSup)
        else:
            result.concat(extraccion_datos_clima(fechaInf, fechaSup))
        # siguiente intervalo de 30 dias
        fechaSup = fechaInf
        fechaInf = subtract30Days(fechaSup)


    return result
