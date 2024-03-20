from transform_main import *
import argparse
from pathlib import Path
def main():
    # Script args
    parser = argparse.ArgumentParser(description="Script para la adquisición y procesamiento de datos.")
    # Obligatorios
    parser.add_argument('--ruta_boya', required=True, help="Ruta del archivo de datos de la boya(df_primario). Especifica el camino completo o relativo al archivo que contiene los datos que se desean procesar.")
    parser.add_argument('--ruta_meteo', required=True, help="Ruta del archivo de datos meteorológicos(df_secundario). Especifica el camino completo o relativo al archivo que contiene los datos que se desean procesar.")
    # Opcional, ruta de salida
    parser.add_argument('--ruta_salida', required=False, help="Ruta para guardar los datos procesados. Indica dónde se desea almacenar el resultado del procesamiento de datos, incluyendo el nombre del archivo de salida.")
    args = parser.parse_args()

    try:
        df_def = transform_main(args.ruta_boya, args.ruta_meteo)
        ruta = args.ruta_salida
        if ruta is None: # si no se especifico la salida, guarda en clean/df_definitivo.parquet
            Path.mkdir("clean", exist_ok=True)
            ruta = "clean/df_definitivo.parquet"
        # Guardamos el conjunto de datos definitivo
        df_def.to_parquet(ruta)
        print("Prerocesamiento de datos se completó exitosamente.")
        print(f"Archivo guardado en {ruta}")
    except Exception as e:
        print(f"Ocurrió un error durante el preprocesamiento de los datos: {e}")



if __name__ == '__main__':
    main()