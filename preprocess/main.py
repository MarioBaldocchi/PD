from transform_meteo import *
from transform_boya import *

def main():
    # Cargamos datos en bruto
    df_principal, df_secundario = pd.read_parquet("raw/fuente_principal.parquet"),  pd.read_parquet("raw/fuente_secundaria.parquet")

    # Preprocesamos por separado
    df_principal = preprocess_boya(df_principal)
    df_secundario = preprocess_meteo(df_secundario)

    # unimos los dos dataframes
    df_def = df_secundario.merge(df_principal, on=['anio', 'mes', 'dia', 'hora']).sort_values(['anio', 'mes', 'dia'], ascending=[True, True, True])

    #vemos que algunas columnas no tienen el tipo correcto
    #print(df_def.dtypes)

    df_def = cambiar_tipo('int', ['Vviento', 'PeriodoOlas', 'Temperatura', 'Nubosidad'], df_def)
    df_def = cambiar_tipo('float', ['AlturaOlas', 'Lluvia'], df_def)

    # Guardamos el conjunto de datos definitivo
    df_def.to_parquet("clean/df_definitivo.parquet")

if __name__ == '__main__':
    main()