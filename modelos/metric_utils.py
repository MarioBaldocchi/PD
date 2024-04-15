"""
Clase que ayuda a calcular las metricas usadas
"""
from sklearn.metrics import *

def calcular_metricas(y_true, y_predict):
    return {
        "TEST_MAX_ERROR": max_error(y_true, y_predict),
        "TEST_ROOT_MEAN_SQ_ERROR": root_mean_squared_error(y_true, y_predict),
        "TEST_MEDIAN_ABS_ERROR": median_absolute_error(y_true, y_predict),
        "TEST_MEAN_ABS_ERROR": mean_absolute_error(y_true, y_predict),
    }

def calcular_metricas_search(search, X_test, y_test):
    # metricas TEST
    metricas = calcular_metricas(y_test, search.best_estimator_.predict(X_test))
    # metricas CV
    ind = search.best_index_
    metricas["CV_TEST_RMSE"] = -1 * search.cv_results_["mean_test_score"][ind]
    metricas["CV_TRAIN_RMSE"] = -1 * search.cv_results_["mean_train_score"][ind]
    return metricas
