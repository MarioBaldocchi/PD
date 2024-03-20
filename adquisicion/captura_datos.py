import requests
import datetime
import pandas as pd

def extraccion_df_meteo(fechaIni, fechaFin):
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

def subtract30Days(date):
    """Resta a la fecha pasada un intervalo de 30 días"""
    return date - datetime.timedelta(days=30)