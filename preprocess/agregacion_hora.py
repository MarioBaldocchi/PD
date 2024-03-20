"""
Archivo para agregación de los datos horarios.
Convertimos dos filas de media hora en una de una hora
"""

def aggregate_secondary(df, key_cols):
    # key_cols: columnas por las que se agrega(dentro de groupby)
    # Diccionario con operaciones de agregacion para cada columna
    # Realizaremos la media para todas las columnas excepto las dummies de direccion de viento, para las cuales nos quedamos con el maximo(lo mismo que OR)
    wdirKey = 'wdir_'
    agg_cols = [c for c in df.columns if c not in key_cols]  # columnas agregadas

    ops = {key: 'mean' for key in agg_cols if key[:len(wdirKey)] != wdirKey}
    ops.update({key: 'max' for key in agg_cols if key[:len(wdirKey)] == wdirKey})
    return df.groupby(key_cols).agg(ops).reset_index()
