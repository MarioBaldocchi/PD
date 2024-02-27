import pandas as pd
import requests
def extraccion_datos_boya():
    """Devuelve un dataFrame con los datos obtenidos de la boya localizada en la playa de Tramore"""
    df = pd.read_csv("./FuentePrincipal.csv", sep = ";", index_col=[0])
    return df

def extraccion_datos_clima(ini, fin):
  """Dado un periodo máximo de 31 días, devuelve los datos climatológicos (por hora) de cada día"""

  fechaIni = int(ini[6:] + ini[3:5] + ini[0:2])
  fechaFin = int(fin[6:] + fin[3:5] + fin[0:2])

  datos = {
    "apiKey": "e1f10a1e78da46f5b10a1e78da96f525",
    "units": "e",
    "startDate": fechaIni,
    "endDate": fechaFin
  }
  tablaWeather = requests.get("https://api.weather.com/v1/location/EIWF:9:IE/observations/historical.json", params=datos).json()
  df = pd.DataFrame.from_dict(tablaWeather["observations"])
  return df

"""def extraccion_df_secundario(fechaIni, fechaFin):
    meses_dias = {'01': ('01', '31'), '02': ('01', '28'), '03': ('01', '31'), '04': ('01', '30'), '05': ('01', '31'), '06': ('01', '30'), '07': ('01', '31'), '08': ('01', '31'), '09': ('01', '30'), '10': ('01', '31'), '11': ('01', '30'), '12': ('01', '31')}
    fechaTmp = fechaIni
    while(fechaIni != fechaFin):
        if(fechaTmp == fechaIni):
            df = extraccion_datos_clima(int(fechaTmp[6:] + fechaTmp[3:5] + fechaTmp[0:2]), int(fechaTmp[6:] + fechaTmp[3:5] + meses_dias[fechaTmp[3:5]][1]))
        else:
            df.concat(extraccion_datos_clima(fechaIni, fechaFin))
        if fechaTmp[3:5] == '12':
            
    return df"""
