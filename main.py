from adquisicion.extraccion_datos import *
from preprocess.transform_1 import quitar_columnas_innecesarias
from preprocess.transform_1 import tratar_na
from preprocess.transform_2 import descomponerTiempoUnix
from preprocess.transform_3 import aggregate_secondary
from preprocess.transform_2 import descomponerHoras
from utils.utils import *

"""OBTENCIÓN DE DATOS EN BRUTO"""
df_principal, df_secundario = extraccion_datos()
for col in df_principal.columns:
    print(col)
    print(df_principal[col].unique())

df_secundario = descomponerTiempoUnix(df_secundario).sort_values(['anio', 'mes', 'dia'], ascending=[True, True, True])


# Movemos la fecha del indice a la columna fecha y la transformamos en formato datetime pandas
df_principal.reset_index(inplace=True)
df_principal = df_principal.rename(columns={"index": 'fecha'})
df_principal.fecha = pd.to_datetime(df_principal.fecha, format = '%d.%m.%Y')

"""TRANSFORMACIÓN DE LOS DATOS"""
#Quitamos las columnas que solo tomen un valor (no aportan información relevante para las predicciones)
df_principal = quitar_columnas_innecesarias(df_principal)
df_secundario = quitar_columnas_innecesarias(df_secundario)

"""Eliminamos columnas del df_secundario:
gust: muchos nan (es preferible quitar la variable antes que eliminar muchas observaciones)
wdir: muchos nan (es preferible quitar la variable antes que eliminar muchas observaciones). PD: la eliminación de la columna wdir no nos afecta porque podemos obtener dicha información 
                                                                                                 a partir de la columna wdir_cardinal, la cual en vez de ser numérica es categórica
day_ind: nos dice si es de noche(N) o de dia(D), lo podemos saber con la hora actual
wx_icon: icono que se usó para la visualización(nube, lluvia)
icon_extd: parecida a wx_icon
clds: nivel de nubosidad, ya esta especidicada con numeros en la fuente principal.
wx_phrase: Frase para describir el tiempo. Se calcula a partir de otras columnas.
uv_desc: Descripcion del estado de ultravioleta. Se saca a aprtir de uv_index. 0-2 Low, 3-5 Moderate, 6-7 High
"""
df_secundario.drop(columns=["day_ind", "wx_icon", "icon_extd", "gust", "wdir", "clds", "wx_phrase", "uv_desc"], inplace=True)


# Convertimos la columnas dirección de viento a variables dummy
# Reemplazamos por NA los datos de wdir_cardinal == CALM para asi no salga en las variables dummy
df_secundario.loc[df_secundario['wdir_cardinal'] == 'CALM', 'wdir_cardinal'] = pd.NA

df_secundario = pd.get_dummies(df_secundario, prefix='wdir', columns=['wdir_cardinal'])

# Agregamos los datos por cada hora (nos quedamos con 1 fila para cada hora)
df_secundario = aggregate_secondary(df_secundario, ['anio', 'mes', 'dia', 'hora'])

#Quitando las columnas anteriormente mencionadas, nos quedan 17 observaciones (filas) con algún na en df_secundario. La mayoría (15) se dan el 1
#de Febrero de 2022 debido a un error del aparato que calcula el uv_index (yo optaría por quitar las observaciones del 1
#de Febrero en df_principal y df_secundario. Las otras dos filas con na también las quitaría, porque son de horas distintas
#(al tener 2 observaciones seguríamos teniendo observaciones para todas las horas)
df_secundario.dropna(inplace=True)  #Quitamos las filas con algún na
df_principal = tratar_na(df_principal) #En el caso de df_principal, los na representan 0's, por lo que los tratamos
# El - indica ausencia algo, ej. viento, por ello podemos reemplazarlo por ceros
df_principal = df_principal.replace('-', 0)

#print(df_principal)

df_principal = descomponerHoras(df_principal)

# unimos los dos dataframes
df_merge = df_secundario.merge(df_principal, on=['anio', 'mes', 'dia', 'hora']).sort_values(['anio', 'mes', 'dia'], ascending=[True, True, True])


