from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd

'''
Saca las predicciones actuales de la fuente primaria y los guarda en el formato del archivo csv
'''
def forecast_primaria_raw():
    browser = webdriver.Firefox()
    df = None
    try:
        browser.get("https://www.windguru.cz/47761")
        delay = 5 # seconds
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'tabid_0_content_div')))
        # sacamos la tabla de predicciones
        dfs = pd.read_html(myElem.get_attribute('innerHTML'))
        df = dfs[0] # primera tabla es la que necesitamos

        # para guardar correctamente el nombre de las columnas, no los indices
        df.columns = df.iloc[0].str.replace(' ', '') # eliminamos espacios en blanco
        df.drop(df.index[0], inplace=True)

        # solo nos quedamos con las mediciones necesarias (filtramos filas)
        df = df[[True, False, False, True, True, False, True, True, True, False, False]]
        df.reset_index(drop=True, inplace=True)

        # los datos de nubosidad es una fila con varias filas(low/mid/high), hacemos la media para quedarnos con un valor
        htmlClouds = myElem.find_element(By.ID, 'tabid_0_0_CDC').get_attribute('outerHTML')
        htmlClouds = htmlClouds.replace('tr', 'table')
        htmlClouds = htmlClouds.replace('td', 'tr')
        htmlClouds = htmlClouds.replace('div', 'td')
        clouds = pd.read_html(htmlClouds)[0]
        # reemplazamos nubosidad con la media de los tres
        df.iloc[4, :] = ((clouds[0] + clouds[1] + clouds[2]) // 3).fillna(0).astype('int')
    finally:
        # cerramos sesion
        browser.close()

    return df


# sacamos la fecha actual
now = datetime.now()
df = forecast_primaria_raw()
df.to_csv('../primaria-raw/' + now.strftime('%Hh_%d_%m_%Y.csv'), index=False)