from sklearn.linear_model import LinearRegression
from train_test_split import separar_train_test
from ml_flow_utils import MLFlow
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

flo = MLFlow("linear")

X_train, X_test, y_train, y_test = separar_train_test()

params = {}

model = LinearRegression(**params)
model.fit(X_train, y_train)

flo.persist_model_to_mlflow(X_train, X_test, y_train, y_test, model, params, "Regresión lineal")

# Probamos mejorar el resultado escalonando

scaler = ColumnTransformer(
    transformers=[
        # no escalonamos las dummy de dirección de viento
        ("num", StandardScaler(), [c for c in X_train.columns if not c.startswith('wdir_')]),
    ]
)

params = {}

pipe = Pipeline([('scaler', scaler), ('lin', LinearRegression(**params))])

pipe.fit(X_train, y_train)

flo.persist_model_to_mlflow(X_train, X_test, y_train, y_test, pipe, params, "Regresión lineal con escalado")