RANDOM_SEED = 777

from modelos.metric_utils import calcular_metricas_search, calcular_metricas
from modelos.subsets_manager import datos_full, sep_train_test, cv_folds
from modelos.mlflow.ml_flow_utils import MLFlow