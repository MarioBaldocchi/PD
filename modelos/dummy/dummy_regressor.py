from sklearn.dummy import DummyRegressor
from sklearn.model_selection import cross_validate

from modelos import *
from modelos.subsets_manager import *

'''
Modelo que solo devuelve la media del train
Será usado como referencia de la peor predicción
'''

flo = MLFlow("dummy")

X_train, X_test, y_train, y_test = sep_train_test()

params = {
    "strategy": "mean"
}

# Create and train models.
model = DummyRegressor(**params)
# Validación cruzada
cv_metrics = cross_validate(model, X_train, y_train, scoring="neg_root_mean_squared_error", return_train_score=True)

model.fit(X_train, y_train)
metricas = calcular_metricas(y_test, model.predict(X_test))
metricas["CV_TEST_RMSE"] = -1 * cv_metrics['test_score'].mean()
metricas["CV_TRAIN_RMSE"] = -1 * cv_metrics['train_score'].mean()

flo.persist_model_to_mlflow(X_train, model, params, metricas,"dummy-mean", "Dummy regression - solo devuelve la media")
