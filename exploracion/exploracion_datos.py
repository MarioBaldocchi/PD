import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
def distribuciones(df):
    for col in df.columns:
        plt.hist(df[col], bins = 12)
        plt.title(col)
        plt.show()

def distribuciones_dummies(df):
    i = 0
    if(len(df.columns) == 17):
        plt.subplots(6,3, figsize = (10,10), constrained_layout=True)
        for col in df.columns:
            plt.subplot(6,3,i + 1)
            plt.hist(df[col])
            plt.title(col)
            i = i + 1
        plt.show()

def correlaciones(df):
    sns.heatmap(data=df.corr(), annot=False)
    plt.show()

def olasPorTiempo(df, year):
    # Vemos las alturas de las olas para cada mes de year
    rows, cols = 4, 3
    fig, axs = plt.subplots(rows, cols)
    fig.suptitle(f"Distribución de olas por meses en {year}")
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    for m in range(1, 13):
        df_tmp = df[(df.anio == year) & (df.mes == m)]
        tiempo = pd.to_datetime(dict(year=df_tmp.anio, month=df_tmp.mes, day=df_tmp.dia, hour=df_tmp.hora))
        ax = axs[(m - 1)//cols, (m - 1) % cols]
        ax.plot(tiempo, df_tmp.AlturaOlas)
        ax.set_xlabel(meses[m - 1])
        ax.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
    plt.show()
