from transform_boya import *
from transform_meteo import *
from transform_lunar import *
from transform_utils import *

def merge_all(path_raw_boya, path_raw_meteo, path_raw_lunar):
    # Cargamos datos en bruto
    df_principal = pd.read_parquet(path_raw_boya)
    df_secundario = pd.read_parquet(path_raw_meteo)
    df_terciario = pd.read_parquet(path_raw_lunar)

    # Preprocesamos por separado
    df_principal = preprocess_boya(df_principal)
    df_secundario = preprocess_meteo(df_secundario)
    df_terciario = preprocess_lunar(df_terciario)

    # unimos los dos dataframes
    df_def = df_secundario.merge(df_principal, on=['anio', 'mes', 'dia', 'hora']).sort_values(['anio', 'mes', 'dia'],
                                                                                              ascending=[True, True,
                                                                                                         True])
    df_def = df_terciario.merge(df_def, on=['anio', 'mes', 'dia']).sort_values(['anio', 'mes', 'dia'],
                                                                                              ascending=[True, True,
                                                                                                         True])
    # vemos que algunas columnas no tienen el tipo correcto
    # print(df_def.dtypes)

    df_def = cambiar_tipo('int', ['Vviento', 'PeriodoOlas', 'Temperatura', 'Nubosidad'], df_def)
    df_def = cambiar_tipo('float', ['AlturaOlas', 'Lluvia'], df_def)

    return df_def

