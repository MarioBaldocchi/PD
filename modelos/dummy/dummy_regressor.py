'''from sklearn.dummy import DummyRegressor

from train_test_split import separar_train_test
from ml_flow_utils import MLFlow
'''
'''
Modelo que solo devuelve la media del train
Será usado como referencia de la peor predicción
'''
'''
flo = MLFlow("dummy")

X_train, X_test, y_train, y_test = separar_train_test()

params = {
    "strategy": "mean"
}

# Create and train models.
model = DummyRegressor(**params)
model.fit(X_train, y_train)

flo.persist_model_to_mlflow(X_train, X_test, y_train, y_test, model, params, "Dummy regression - solo devuelve la media")
'''