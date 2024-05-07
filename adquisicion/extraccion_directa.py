from adquisicion.captura_datos_lunar import adquirir_terciaria
from adquisicion.captura_datos_meteo import extraccion_df_meteo
from adquisicion.capturar_datos_boya import caturar_datos_boya


def extraccion_directa(fechaIni, fechaFin):
    # fechas en formato yyyy-mm-dd -> '2024-01-01', '2024-05-07'
    df_luna = adquirir_terciaria(fechaIni, fechaFin)
    df_luna.to_parquet('../raw/fuente_terciaria.parquet', index=False)

    df_meteo = extraccion_df_meteo(fechaIni, fechaFin)
    df_meteo.to_parquet('../raw/fuente_secundaria.parquet')

    df_boya = caturar_datos_boya(fechaIni, fechaFin)
    df_boya.to_parquet('../raw/fuente_principal.parquet')


extraccion_directa('2024-01-01', '2024-01-02')