# spectredash/state.py

from shiny import reactive

# Shared reactive values
shared_first_choice = reactive.Value(None)
shared_second_choice = reactive.Value(None)
