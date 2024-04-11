import mlflow
from mlflow.models import infer_signature
from sklearn.metrics import max_error, root_mean_squared_error, median_absolute_error, mean_absolute_error
'''
Clase que se encarga de guardar el modelo con sus resultados a MLFlow
'''
class MLFlow:
    def __init__(self, exp_title):
        '''
        @param exp_title: nombre del experimento
        '''
        #mlflow.sklearn.autolog() - selecciona automaticamente las metricas a guardar
        mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
        mlflow.set_experiment(exp_title)

    def calcular_metricas(self, y_true, y_predict):
        return {
            "MAX_ERROR": max_error(y_true, y_predict),
            "ROOT_MEAN_SQ_ERROR": root_mean_squared_error(y_true, y_predict),
            "MEDIAN_ABS_ERROR": median_absolute_error(y_true, y_predict),
            "MEAN_ABS_ERROR": mean_absolute_error(y_true, y_predict),
        }

    def persist_model_to_mlflow(self, X_train, X_test, y_train, y_test, model, params, train_info=""):
        """
        @param X_train: matrix, variables explicativas del conjunto TRAIN
        @param y_train: matrix, variable respuesta del conjunto TRAIN
        @param X_test: matrix, variables explicativas del conjunto TEST
        @param y_test: array, variable respuesta del conjunto TEST

        @param model: objeto, el modelo ya ENTRENADO
        @param params: diccionario, los hiperparametros del modelo

        @param train_info: string, la descripción del entrenamiento del modelo (para identificarlo)
        """
        # Start an MLflow run
        with mlflow.start_run():
            # Log the hyperparameters
            mlflow.log_params(params)

            # Log the loss metric
            mlflow.log_metrics(self.calcular_metricas(y_test, model.predict(X_test)))

            # Set a tag that we can use to remind ourselves what this run was for
            mlflow.set_tag("Training Info", train_info)

            # Infer the model signature
            signature = infer_signature(X_train, model.predict(X_train))

            # Log the model
            model_info = mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="wave_height",
                signature=signature,
                input_example=X_train,
                #registered_model_name=train_info,
            )