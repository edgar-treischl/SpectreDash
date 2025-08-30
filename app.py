from shiny import App, ui

app_ui = ui.page_navbar(  
    ui.nav_panel("A", "Page A content"),  
    ui.nav_panel("B", "Page B content"),  
    ui.nav_panel("C", "Page C content"),  
    title="App with navbar",  
    id="page",  
)  




app_ui = ui.page_fillable(
    # Card structure with Sidebar
    ui.card(
        ui.card_header("Card with Sidebar and Navbar"),  # Header of the card
        ui.layout_sidebar(  
            # Sidebar content
            ui.sidebar("Sidebar", bg="#f8f8f8"),  
            # Main content area of the sidebar card (can have other content)
            ui.navbar(
                ui.nav_panel("A", "Page A content"),  # Panel for Page A
                ui.nav_panel("B", "Page B content"),  # Panel for Page B
                ui.nav_panel("C", "Page C content"),  # Panel for Page C
                title="App with Navbar",  # Title for the navbar
                id="page",  # ID for the navbar
            ),
        ),
    )
)

# Create the app with the combined UI
app = App(app_ui)

if __name__ == "__main__":
    app.run()
