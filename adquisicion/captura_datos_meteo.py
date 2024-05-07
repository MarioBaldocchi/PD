import requests
import datetime
import pandas as pd

def extraccion_df_meteo(fechaIni, fechaFin):
    # fechaIni y fechaFin en formato 2024-02-07 (%Y-%m-%d)
    result = None
    fechaIni = stringToDatetime(fechaIni)
    fechaFin = stringToDatetime(fechaFin)
    # realizaremos consultas a la api de la forma extraccion_meteo_api(fechaInf, fechaSup)
    fechaSup = fechaFin
    fechaInf = subtract30Days(fechaSup)
    while(fechaIni < fechaSup):
        if (fechaIni > fechaInf):
            # intervalo menor de 30 días
            # fechaInf < fechaIni -> intervalo [fechaIni, fechaSup]
            fechaInf = fechaIni

        if result is None:
            result = extraccion_meteo_api(fechaInf, fechaSup)
        else:
            result = pd.concat([result, extraccion_meteo_api(fechaInf, fechaSup)])
        # siguiente intervalo de 30 dias
        fechaSup = fechaInf
        fechaInf = subtract30Days(fechaSup)

    return result

def extraccion_meteo_api(ini, fin):
  """Dado un periodo, máximo 31 días, devuelve los datos climatológicos (por hora) de cada día"""
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


def stringToDatetime(string):
    """Transforma la fecha en formato año-mes-dia ('2024-01-21') al objeto datetime"""
    return datetime.datetime.strptime(string, "%Y-%m-%d")

'''
df = extraccion_df_meteo('2024-01-01', '2024-05-07')
df.to_parquet('../raw/fuente_secundaria.parquet')
'''