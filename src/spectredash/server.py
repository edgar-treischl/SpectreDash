from shiny import App, render, ui
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset from seaborn (you can replace 'iris' with any available dataset)
df = sns.load_dataset('penguins')  # Replace with your dataset name if needed

def app_server(input, output, session):
    @render.plot
    def hist():
        p = sns.histplot(df, x=input.var(), facecolor="#007bc2", edgecolor="white")
        return p.set(xlabel=None)

    @render.data_frame
    def data():
        return df[["species", "island", input.var()]]
