# from spectredash.plots import plot_pipe
# from plotnine import ggplot
# import matplotlib.pyplot as plt

# def test_plot_pipe():
#     table_name = "penguins"  # Replace with a valid table name in your DuckDB

#     try:
#         plot_obj = plot_pipe()
#     except Exception as e:
#         print(f"Error calling plot_pipe: {e}")
#         return

#     # Check if the result is a ggplot object
#     if not isinstance(plot_obj, ggplot):
#         print("Returned object is NOT a ggplot object.")
#         return
#     else:
#         print("plot_pipe returned a ggplot object successfully!")

#     # Render the plot with matplotlib (plotnine backend)
#     fig = plot_obj.draw()  # Returns a matplotlib Figure

#     # Show the plot (this will open a window if run locally)
#     plt.show()

# if __name__ == "__main__":
#     test_plot_pipe()
