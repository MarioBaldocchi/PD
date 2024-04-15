'''
Clase encargada de separar los datos en:
- Test (datos de 2023)
- Train (datos de 2022)
    - K folds (para validación)
'''
import pandas as pd
from sklearn.model_selection import KFold
from modelos import RANDOM_SEED

'''
Devuelve el conjunto de datos completo:
matriz de variables explicativas, matriz de variable respuesta
'''
def datos_full():
    df = pd.read_parquet("../../clean/df_definitivo.parquet")
    target = "AlturaOlas"
    X = df.drop(columns=target)
    y = df[target]
    return X, y

'''
Devuelve:
X_train, X_test, y_train, y_test
'''
def sep_train_test():
    X, y = datos_full()
    filtro_test = (X.anio == 2023)
    return X[~filtro_test], X[filtro_test], y[~filtro_test], y[filtro_test]


K = 5

'''
Devuelve:
KFold con el numero de folds predeterminado con K
'''
def cv_folds():
    return KFold(n_splits=K, shuffle=True, random_state=RANDOM_SEED)