from shiny import App, render, ui
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset from seaborn (you can replace 'iris' with any available dataset)
df = sns.load_dataset('penguins')  # Replace with your dataset name if needed

def app_server(input, output, session):
    @render.plot
    def hist():
        # Get the hue based on the 'species' input or None if not provided
        hue = "species" if input.species() else None
        
        # Plot the KDE (Kernel Density Estimation) with seaborn
        sns.kdeplot(df, x=input.var(), hue=hue)
        
        # Optionally add a rug plot if the 'show_rug' input is True
        if input.show_rug():
            sns.rugplot(df, x=input.var(), hue=hue, color="black", alpha=0.25)
        
        # Ensure the plot is displayed properly
        #plt.show()
