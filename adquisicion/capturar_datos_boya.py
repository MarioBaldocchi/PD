import requests
import pandas as pd
from datetime import datetime
'''
Le cambia el nombre de las columnas para que sea mas facil preprocesar
'''
def boya_set_columns(tableWaves):
    trans_dict = {
        'Wind speed (knots)': 'Vviento',
        'Wave (m)': 'AlturaOlas',
        'Wave period (s)': 'PeriodoOlas',
        'Temperature (°C)': 'Temperatura',
        'Rain (mm/1h)': 'Lluvia',
        'Cloud cover (%)': 'Nubosidad',
    }
    df = tableWaves.copy()
    # cambiamos los nombres de columnas a una palabra
    df.iloc[0] = df.iloc[0].replace(trans_dict)
    # eliminamos h de las horas
    columnas = df.iloc[1]
    columnas = columnas.str.replace('h', '')
    df.columns = df.iloc[0] + columnas
    df.drop([0,1], axis=0, inplace=True)
    df.set_index(df.columns[0], drop=True, inplace=True)
    df.index.name = None
    return df

'''
Saca datos historicos de la boya
'''
def caturar_datos_boya(first_date, last_date):
    # first_date y last_date en formato 2024-02-07 (%Y-%m-%d)
    url = 'https://www.windguru.cz/ajax/ajax_archive.php'

    headers = {
        'Cookie': 'idu=1886609; login_md5=4978173d9ab813364b25e7fd32513b03',
    }
    data = {
        'date_from': first_date,
        'date_to': last_date,
        'step': '1',
        'min_use_hr': '6',
        'pwindspd': '1',
        'phtsgw': '1',
        'pperpw': '1',
        'ptmp': '1',
        'papcp': '1',
        'ptcdc': '1',
        'id_spot': '47761',
        'id_model': '3',
        'id_stats_type': ''
    }

    response = requests.post(url, headers=headers, data=data)

    tableWaves = pd.read_html(response.content)[1]
    return boya_set_columns(tableWaves)

'''
df = caturar_altura_olas('2024-01-01', '2024-05-07')
df.to_parquet('../raw/fuente_principal.parquet')
'''