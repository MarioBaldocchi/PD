
![image](https://github.com/MarioBaldocchi/PD/assets/118186855/df659a18-929d-48c8-b30d-f4d3f70ca0ee)

## Tabla de contenidos
* [Misión](#misión)
* [Installación y Setup](#installación-y-setup)
* [Datos](#datos)
* [Evaluación sobre predicciones](#evaluación-sobre-predicciones)
### Misión
Nuestra principal misión es realizar predicciones de las alturas de las olas en la playa de Tramore (Irlanda) para mejorar la experiencia de los surfistas.
Para ello, nos apoyamos en distintas fuentes como páginas web climatológicas y oceanográficas.

# Installación y Setup
## Python y paquetes usados (summary requirements.txt)
- **Python `v3.11`**
- **Data Manipulation:** `pandas`, `numpy`
- **Data Visualization:** `matplotlib`
- **Data Mining:** `requests`, `json`, `Path`

## Creación entorno virtual
Creamos el entorno virtual en la carpeta venv(ejecutamos desde la raiz del proyecto)

`python -m venv venv`

Activamos el entorno (siempre al empezar a trabajar)

Windows:

`venv\Scripts\activate.bat`

Linux/Mac:

`source venv/bin/activate`

Estando en esa consola con el entorno activo, instalamos los modulos necesarios

`pip install -r requirements.txt`

## Setup del programa
Carga de datos del drive (a la carpeta raw, especidicado en archivos_info.txt)

`python ./adquisicion/main.py`

Preprocesamiento de datos, especificando los parámetros

`python ./preprocess/main.py --ruta_boya ./raw/fuente_principal.parquet --ruta_meteo ./raw/fuente_secundaria.parquet --ruta_lunar  ./raw/fuente_terciaria.parquet`

Inicializar programa

`python main.py`
## Uso de jupyter con el entorno virtual
Para ejecutarlo desde el entorno virtual

`python -m jupyter notebook`
## Uso de mlflow
### Levantamiento del servidor
Los resultados se guardarán en el archivo mlruns.db

`mlflow ui --port 5000 --backend-store-uri sqlite:///mlruns.db`
### Guardar un modelo
Entrenamos el modelo
```
flo = MLFlow(<nombre de la técnica usada (regresion lineal/ arboles de decisión...)>)
params = {}
model = LinearRegression(**params)
model.fit(X_train, y_train)
```

Calcula las métricas y las guarda en mlflow


`flo.persist_model_to_mlflow(X_train, X_test, y_train, y_test, model, params, "Regresión lineal")`
# Datos
## Source Data
-Link de donde se han obtenido los datos de la boya: 
https://www.windguru.cz/archive.php?id_spot=47761&id_model=3&date_from=2023-01-01&date_to=2024-01-01

-Link de donde se obtienen los datos climatológicos mediante la api:
"https://api.weather.com/v1/location/EIWF:9:IE/observations/historical.json"

## Data Acquisition
Los datos se obtienen de google drive, nuestra base de datos. Estos habían sido obtenidos previamente a través de los links anteriormente mencionados.

## Data Preprocessing
El preprocesamiento se divide en las siguientes etapas:
- **Eliminación de columnas irrelevantes**: Se eliminan todas aquellas variables que toman un único valor o tienen todo nulos.
- **Tratamiento de nulos**: En cuanto a nuestra fuente principal, los nulos realemte representas 0´s, por lo que simplemente reemplazamos todos lo nulos por 0. Sin embargo, hay nulos ocultos, que vienen representados por guiones (-). Al haber pocas observaciones con nulos, decidimos eliminarlas. Referente a la fuente secundaria, tan sólo hay dos variables con muchos nulos: `gus`´ y `wdir`. Decidimos eliminar dichas variables puesto que si optamos por eliminar las observaciones que contienen algún nulo, nuestra base de datos se reduciría más de un 80%. La imputación hemos decidido descartarlas por la gran cantidad de nulos presentes en dichas variables. Una vez quitadas las variables, nos quedan 17 nulos concentrados el 1 de febrero de 2022, suponemos que se debe a un mal funcionamiento de los aparatos de medición. En este caso, eliminamos las observaciones con algún nulo.
- **Tratamiento de nulos**

## Evaluación sobre predicciones
Dado que nos basaremos en predicciones de otros datos para predecir la altura de la ola,
para evaluar el rendimiento del sistema de forma más aproximada a la situación real posible
hemos recolectado predicciones de diferentes días/horas que se guardan en la carpeta forecasts-preprocess.
Con el código de  preprocesado en esa misma carpeta sacamos la antelación de las predicciones
para posteriormente evaluar el rendimiento en función de la antelación.

# Estructura del proyecto

```
├── adquisicion (lógica de captura de la api/descarga de los datos del drive)
├── preprocess (lógica de preprocesado y limpieza de los datos)
├── metadata (descripción de los datos)
├── forecasts (aduisicion, almacenamiento y preprocesado de los datos de predicciones(NO reales))
│    ├── preprocess_forecast_primaria.ipynb - preprocesamiento de datos para la fuente primaria
│    ├── preprocess_forecast_secundaria.ipynb - preprocesamiento de datos para la fuente secundaria
│    ├── primaria-raw - continene los archivos de predicciones de fuente primaria
│    │                cuyo nombre representa la fecha y hora(sin minutos) en la que se hizo la predicción, ej 13h_03_05_2024.csv
│    └── secundaria-raw - continene los archivos de predicciones de fuente secundaria
│                     cuyo nombre representa la fecha y hora(sin minutos) en la que se hizo la predicción, ej 13h_03_05_2024.csv
│
├── modelos (entrenamiento y evaluacion de modelos)
│    ├── modelo_definitivo - carpeta que guarda el modelo definitivo en el formato pickle, que se usará en producción
│    ├── metrics_utils.py - ayuda a calcular las métricas de evalución
│    ├── ml_flow_utils.py - ayuda a guardar el modelo en MLFLow o cargarlo de ahi
│    ├── subsets_manager.py - clase encargada de separar los datos en subconjuntos train, validacion y test
│    ├── analisis.ipynb - notebook que analiza los datos para sacar conclusiones (antes entrenar los modelos)
│    │
│    ├── evaluacion (evaluacion de los modelos obtenidos)
│    │    ├── runs (guarda las ejecuciones exportadas de mlflow para evaluar de forma mas facil los modelos)
│    │    │
│    │    ├── evaluacion-lineales.ipynb (evaluacion de los modelos lineales)
│    │    ├── evaluacion-forest.ipynb (evaluacion de los modelos que usan random forest)
│    │    ├── evaluacion-mlp.ipynb (evaluacion de los modelos de MLP)
│    │    │
│    │    └── evaluacion-best.ipynb (eligiendo el mejor modelo)
│    │
│    │ (en las siguentes subcarpetas hay notebooks para entrenar los modelos asociados)
│    ├── dummy (modelo que solo devuelve la media, sin importar el input)
│    ├── lineal (entrenamiento de varios tipos de modelos lineales)
│    ├── mlperceptron (entrenamiento del modelo de MLP (redes neuronales))
│    └── random_forest (entrenamiento del modelo de random forest)
│    
├── utils (herramientas de uso adicional)
└── exploracion
```
