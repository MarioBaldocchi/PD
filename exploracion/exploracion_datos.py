import matplotlib.pyplot as plt
import seaborn as sns
def distribuciones(df):
    for col in df.columns:
        plt.hist(df[col], bins = 12)
        plt.title(col)
        plt.show()

def correlaciones(df):
    sns.heatmap(data=df.corr(), annot=False)
    plt.show()
