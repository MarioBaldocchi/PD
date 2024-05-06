'''
Clase encargada de separar los datos en:
- Test (datos de 2023)
- Train (el resto)
    - K folds (para validación)
'''
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from modelos import RANDOM_SEED

'''
Devuelve el conjunto de datos completo:
matriz de variables explicativas, matriz de variable respuesta
'''
def datos_full():
    df = pd.read_parquet("../clean/df_definitivo.parquet")
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

'''
Devuelve el scaler
'''
def get_scaler():
    X_train, X_test, y_train, y_test = sep_train_test()
    X_train = X_train.drop(columns=["Temperatura", 'wspd', 'anio', 'mes', 'dia', 'hora'])
    scaler = ColumnTransformer(
        transformers=[
            # no escalonamos las dummy de dirección de viento
            ("num", StandardScaler(), [c for c in X_train.columns if not c.startswith('wdir_')]),
        ],
        remainder='passthrough'
    )
    scaler.fit(X_train)

    return scaler

'''
Devuelve:
KFold con el numero de folds predeterminado con K
'''
def cv_folds():
    K = 5
    return KFold(n_splits=K, shuffle=True, random_state=RANDOM_SEED)