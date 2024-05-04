import requests
import pandas as pd
from datetime import datetime
'''
Saca las predicciones actuales de la fuente secundaria y los guarda en el formato del archivo json
'''
def forecast_secundaria_raw():
    datos = {
        "apiKey": "e1f10a1e78da46f5b10a1e78da96f525",
        "units": "e",
        "language": "en-US",
        "format": "json",
        "geocode": "52.261,-7.112"
    }
    url = 'https://api.weather.com/v3/wx/forecast/hourly/15day'
    tablaWeather = requests.get(url, params=datos).json()
    return pd.DataFrame.from_dict(tablaWeather)

# sacamos predicciones
df = forecast_secundaria_raw()
# sacamos la fecha actual
now = datetime.now()
# guardamos el dato sacado con la fecha en el nombre del archivo
df.to_json('../secundaria-raw/' + now.strftime('%Hh_%d_%m_%Y.json'), index=False)