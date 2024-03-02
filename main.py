from adquisicion.extraccion_datos import *
from preprocess.transformacion_datos import quitar_columnas_innecesarias
from preprocess.transformacion_datos import tratar_na
from preprocess.transformacion_datos import descomponerTiempo
from utils.utils import *

"""OBTENCIÓN DE DATOS EN BRUTO"""
df_principal = extraccion_datos()
df_secundario = extraccion_df_secundario(stringToDatetime("01/01/2022"), stringToDatetime("31/12/2023"))
df_secundario = descomponerTiempo(df_secundario).sort_values(['anio', 'mes', 'dia'], ascending=[True, True, True])


"""TRANSFORMACIÓN DE LOS DATOS"""
#Quitamos las columnas que solo tomen un valor (no aportan información relevante para las predicciones)
df_principal = quitar_columnas_innecesarias(df_principal)
df_secundario = quitar_columnas_innecesarias(df_secundario)

#En general el df_secundario no tiene muchos na. Sin embargo, las columnas gust y wdir tienen demasiados, por lo que
#en vez de eliminar observaciones, optamos por quitar las columnas. PD: la eliminación de la columna wdir no nos afecta
#porque podemos obtener dicha información a partir de la columna wdir_cardinal, la cual en vez de ser numérica es categórica (OneHotEncoding)
df_secundario.drop(columns=['gust', 'wdir'], inplace=True)

#Quitando las columnas anteriormente mencionadas, nos quedan 17 observaciones (filas) con algún na en df_secundario. La mayoría (15) se dan el 1
#de Febrero de 2022 debido a un error del aparato que calcula el uv_index (yo optaría por quitar las observaciones del 1
#de Febrero en df_principal y df_secundario. Las otras dos filas con na también las quitaría, porque son de horas distintas
#(al tener 2 observaciones seguríamos teniendo observaciones para todas las horas)
df_secundario.dropna(inplace=True)  #Quitamos las filas con algún na
df_principal = tratar_na(df_principal) #En el caso de df_principal, los na representan 0's, por lo que los tratamos

#Comprobacion de que no hay na en df_secundario y df_principal
print(f'df_secundario: {df_secundario.isna().sum()}')
print(f'df_principal: {df_principal.isna().sum()}')

for col in df_secundario.columns:
    print(col, df_secundario[col].unique())