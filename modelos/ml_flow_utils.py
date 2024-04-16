import mlflow
from mlflow.models import infer_signature

from modelos import RANDOM_SEED

'''
Clase que se encarga de guardar el modelo con sus resultados a MLFlow
'''
class MLFlow:
    def __init__(self, exp_title = None):
        '''
        @param exp_title: nombre del experimento
        '''
        #mlflow.sklearn.autolog() - selecciona automaticamente las metricas a guardar
        mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
        if exp_title is not None:
            mlflow.set_experiment(exp_title)

    def get_saved_model(self, model_name):
        return mlflow.pyfunc.load_model(f"models:/{model_name}/latest")

    def persist_model_to_mlflow(self, X_train, model, params, metrics, run_name, train_info=""):
        """
        @param X_train: matrix, variables explicativas del conjunto TRAIN
        @param model: objeto, el modelo ya ENTRENADO
        @param params: diccionario, los hiperparametros del modelo
        @param metrics: diccionario, las metricas que se quieren guardar (ej. {"TEST_ECM": 0.298})

        @param train_info: string, la descripción del entrenamiento del modelo (para identificarlo)
        """
        # Start an MLflow run
        with mlflow.start_run(run_name = run_name):
            # Log the hyperparameters
            mlflow.log_params(params)

            # Log the loss metric
            mlflow.log_metrics(metrics)
            mlflow.log_metric("RANDOM SEED", RANDOM_SEED)
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
                registered_model_name=run_name,
            )