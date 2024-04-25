"""
Clase que ayuda a calcular las metricas usadas
"""
from sklearn.metrics import *

'''
Calcula las métricas usadas para la evalución
'''
def calcular_metricas(y_true, y_predict):
    return {
        "TEST_MAX_ERROR": max_error(y_true, y_predict),
        "TEST_ROOT_MEAN_SQ_ERROR": root_mean_squared_error(y_true, y_predict),
        "TEST_MEDIAN_ABS_ERROR": median_absolute_error(y_true, y_predict),
        "TEST_MEAN_ABS_ERROR": mean_absolute_error(y_true, y_predict),
    }

'''
Calcula las metricas del conjunto TEST para un GridSearch o RandomSearch entrenado (despues de .fit)
'''
def calcular_metricas_search(search, X_test, y_test):
    # metricas TEST
    metricas = calcular_metricas(y_test, search.best_estimator_.predict(X_test))
    # metricas CV
    ind = search.best_index_
    metricas["CV_TEST_RMSE"] = -1 * search.cv_results_["mean_test_score"][ind]
    metricas["CV_TRAIN_RMSE"] = -1 * search.cv_results_["mean_train_score"][ind]
    return metricas

'''
Calcula las metricas del conjunto TEST para un GridSearch o RandomSearch entrenado (despues de .fit)
Ademas, desescala las predicciones, pues los modelos que se pasan se han entrenado con la y escalada
'''
def calcular_metricas_search_escalando_y(search, X_test, y_test, scaler_y):

    predicciones = search.best_estimator_.predict(X_test)
    #Invertimos la escala de las predicciones
    predicciones_best_model_2d = predicciones.reshape(-1, 1)
    predicciones_2d = scaler_y.inverse_transform(predicciones_best_model_2d)

    # metricas TEST
    metricas = calcular_metricas(y_test, predicciones_2d)
    # metricas CV
    ind = search.best_index_
    metricas["CV_TEST_RMSE"] = -1 * search.cv_results_["mean_test_score"][ind]
    metricas["CV_TRAIN_RMSE"] = -1 * search.cv_results_["mean_train_score"][ind]
    return metricas