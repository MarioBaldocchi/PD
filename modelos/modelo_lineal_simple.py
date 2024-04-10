from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from ml_flow_utils import MLFlow

flo = MLFlow("regression")
RANDOM_STATE = 777
db = load_diabetes()

X_train, X_test, y_train, y_test = train_test_split(db.data, db.target, random_state=RANDOM_STATE)

params = {}

# Create and train models.
model = LinearRegression(**params)
model.fit(X_train, y_train)

flo.persist_model_to_mlflow(X_train, y_train, X_test, y_test, model, params, "Regresión lineal")