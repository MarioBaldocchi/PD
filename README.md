Trabajo de Proyectos de Datos 2023-2024

![image](https://github.com/MarioBaldocchi/PD/assets/118186855/df659a18-929d-48c8-b30d-f4d3f70ca0ee)

## Tabla de contenidos
* [Misión](#misión)
* [Installación y Setup](#installación-y-setup)
* [Datos](#datos)
### Misión
Nuestra principal misión es realizar predicciónes de las alturas de las olas para mejorar la experiencia de los surfistas

# Installación y Setup
## Python y packetes usados (summary requirements.txt)
- **Python `v3.11`**
- **Data Manipulation:** `pandas`, `numpy`
- **Data Visualization:** `matplotlib`
- **Data Mining:** `requests`

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

Inicializar programa

`python main.py`


# Datos
## Source Data
Link de donde se han obtenido los datos de la boya: https://www.windguru.cz/archive.php?id_spot=47761&id_model=3&date_from=2023-01-01&date_to=2024-01-01


## Data Acquisition

## Data Preprocessing


# Estructura del proyecto

```bash
├── data
│   ├── data1.csv
│   ├── data2.csv
│   ├── cleanedData
│       ├── cleaneddata1.csv
|       └── cleaneddata2.csv
├── data_acquisition.py
├── data_preprocessing.ipynb
├── data_analysis.ipynb
├── data_modelling.ipynb
├── README.md
└── .gitignore
```
