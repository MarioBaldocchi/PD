from sklearn.linear_model import LinearRegression
from train_test_split import separar_train_test
from ml_flow_utils import MLFlow

flo = MLFlow("regression")

X_train, X_test, y_train, y_test = separar_train_test()

params = {}

# Create and train models.
model = LinearRegression(**params)
model.fit(X_train, y_train)

flo.persist_model_to_mlflow(X_train, X_test, y_train, y_test, model, params, "Regresión lineal")