import requests
import pandas as pd
from datetime import datetime
'''
Saca las predicciones actuales de la fuente secundaria y los guarda en el formato del archivo json
'''
def forecast_terciaria_raw(date_from, date_to):
    # date_from y date_to en este formato 2024-05-01 (yyyy-mm-dd)
    df = None
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/tramore/{date_from}/{date_to}?unitGroup=us&include=days&elements=datetime%2Cmoonphase&key=BQ2F7KDTC7FDZBGWY8JNBH3M2&contentType=json"
    response = requests.request("GET", url)
    if response.status_code != 200:
        print('Error al preprocesar los datos ', response.status_code)
    else:
        # Parse the results as JSON
        jsonData = response.json()
        df = pd.DataFrame.from_dict(jsonData['days'])
    return df

now = datetime.now()
# sacamos predicciones
df = forecast_terciaria_raw(now.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d'))
# guardamos el dato sacado con la fecha en el nombre del archivo
df.to_json('../terciaria-raw/' + now.strftime('%d_%m_%Y.json'), index=False)