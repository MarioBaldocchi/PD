import matplotlib.pyplot as plt
import seaborn as sns
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
