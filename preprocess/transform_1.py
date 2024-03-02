"""
Archivo para preprocesamiento ligero de los datos,
sin pérdida de información
"""

def quitar_columnas_innecesarias(df):
    """Quita todas las columnas que tomen un solo valor. También quita columnas que tienen todo nulos. Devuelve el dataframe transformado"""
    for col in df.columns:
        if len(df[col].unique()) == 1:
            df = df.drop(columns=col)
    return df


def tratar_na(df):
    """Sustituye los nas del dataframe por 0's"""
    for col in df.columns:
        df[col] = df[col].fillna(0) #fixme Revisar cuando los dataframes esten unidos
    return df