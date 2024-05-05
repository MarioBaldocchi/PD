'''
Sirve para capturar observaciones de la altura de las olas
'''

import pandas as pd
import requests

'''
Preprocesa los datos de la altura de olas a partir de una tabla que tiene las horas como columnas
              00h   01h   02h   03h ...
02.05.2024    0.3   0.4   0.3   0.2 ...
03.05.2024    0.2   0.5   0.3   0.1 ...
'''
def preprocess(tableWaves):
    dfs = []
    for col in tableWaves.columns:
        hora = int(col.replace('h', ''))  # sacamos hora
        df = tableWaves[[col]]
        df.columns = ['AlturaOlas']  # renombramos la columna
        df = df[~df.map(lambda x: x == '-').any(axis=1)]
        df['AlturaOlas'] = df['AlturaOlas'].astype('float')
        df.reset_index(inplace=True, names='fecha')
        df['hora'] = hora
        # separamos fecha en varias columnas
        df[['dia', 'mes', 'anio']] = df.fecha.str.split('.', n=3, expand=True)
        df['hora'] = df['hora'].astype('int')
        df['dia'] = df['dia'].astype('int')
        df['mes'] = df['mes'].astype('int')
        df['anio'] = df['anio'].astype('int')
        df.drop(columns=['fecha'], inplace=True)

        dfs.append(df)

    return pd.concat(dfs, axis=0)

'''
Captura las alturas de las olas observadas(reales) entre las fechas indicadas
'''
def caturar_altura_olas(first_day, last_day):
    url = 'https://www.windguru.cz/ajax/ajax_archive.php'

    headers = {
        'Cookie': 'idu=1886609; login_md5=4978173d9ab813364b25e7fd32513b03',
    }
    data = {
        'date_from': f'{int(first_day["anio"])}-{int(first_day["mes"]):02}-{int(first_day["dia"]):02}',
        'date_to': f'{int(last_day["anio"])}-{int(last_day["mes"]):02}-{int(last_day["dia"]):02}',
        'step': '1',
        'min_use_hr': '6',
        'arch_params[]': 'HTSGW',
        'id_spot': '47761',
        'id_model': '84',
        'id_stats_type': '',
    }

    response = requests.post(url, headers=headers, data=data)

    tableWaves = pd.read_html(response.content)[1].iloc[1:]
    tableWaves.columns = tableWaves.iloc[0]
    tableWaves.drop(tableWaves.index[0], inplace=True)
    tableWaves.set_index(tableWaves.columns[0], drop=True, inplace=True)

    return preprocess(tableWaves)