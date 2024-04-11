import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_STATE = 777

'''
Devuelve X_train, X_test, y_train, y_test
'''
def separar_train_test():
    df = pd.read_parquet("../clean/df_definitivo.parquet")
    y_name = "AlturaOlas"
    X = df.drop(columns=y_name)
    y = df[y_name]
    return train_test_split(X, y, random_state=RANDOM_STATE)
