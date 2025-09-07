from shiny import module, reactive, render, ui
import emoji
from plotnine import ggplot
from spectredash.plots import plot_PresenceMatrixWeb
from spectredash.utils import shared_first_choice


@module.ui
def variables_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.h4(f"{emoji.emojize(':bullseye:')} Variables", class_="m-0"),
            ui.row(
                ui.column(
                    3,
                    ui.card(
                        ui.p(
                            "Which variables are included in the data? This view helps compare column presence across different dataset versions."
                        ),
                        ui.tags.ul(
                            ui.tags.li("Each row represents a dataset version."),
                            ui.tags.li("Each column represents a variable."),
                            ui.tags.li(
                                "Green cells indicate presence; red indicate absence."
                            ),
                        ),
                        ui.p(
                            {"class": "text-muted small"},
                            "Use this to detect schema drift or inconsistencies over time.",
                        ),
                    ),
                ),
                ui.column(
                    9,
                    ui.card(
                        ui.div(
                            {"style": "overflow-x: auto"},
                            ui.output_ui("presence_plot_ui"),
                        )
                    ),
                ),
            ),
        )
    )


@module.server
def variables_server(input, output, session):
    plot_state = reactive.Value({"success": True, "error": None, "plot": None})

    @reactive.Calc
    def presence_plot():
        user_table = shared_first_choice.get()

        if not user_table:
            return {"success": False, "error": "No dataset selected.", "plot": None}

        try:
            plot_obj = plot_PresenceMatrixWeb(table=user_table)
            return {"success": True, "plot": plot_obj, "error": None}
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating plot for '{user_table}': {str(e)}",
                "plot": None,
            }

    @reactive.Effect
    def update_state():
        plot_state.set(presence_plot())

    @output
    @render.ui
    def presence_plot_ui():
        result = plot_state.get()
        if result["success"] and isinstance(result["plot"], ggplot):
            return ui.div(
                ui.output_plot("presence_matrix_plot", width="100%", height="500px")
            )
        else:
            return ui.div(
                {
                    "class": "d-flex flex-column justify-content-center align-items-center",
                    "style": "min-height: 400px; background-color: #f8f9fa;",
                },
                ui.tags.i(class_="fas fa-exclamation-circle text-warning fa-4x mb-3"),
                ui.h4("Plot Not Available", class_="text-danger"),
                ui.p(result["error"], class_="text-muted text-center"),
            )

    @output
    @render.plot(alt="Presence Matrix")
    def presence_matrix_plot():
        result = plot_state.get()
        return result["plot"] if result["success"] else None
