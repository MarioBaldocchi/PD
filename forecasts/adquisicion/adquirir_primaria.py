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
        #dfs = pd.read_html(myElem.find_element(By.CLASS_NAME, "tabulka").get_attribute('outerHTML'))
        dfs = pd.read_html(myElem.get_attribute('innerHTML'))
        df = dfs[0] # primera tabla es la que necesitamos
        # para guardar correctamente el nombre de las columnas, no los indices
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace=True)
    finally:
        # cerramos sesion
        browser.close()

    return df


# sacamos la fecha actual
now = datetime.now()
df = forecast_primaria_raw()
df.to_csv('../primaria-raw/' + now.strftime('%Hh_%d_%m_%Y.csv'), index=False)