from shiny import module, reactive, render, ui
import emoji
from plotnine import ggplot
from spectredash.plots import plot_LabelMatrix
from spectredash.utils import shared_first_choice


@module.ui
def labels_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.h4(f"{emoji.emojize(':label:')} Labels", class_="m-0"),
            ui.row(
                ui.column(
                    3,
                    ui.card(
                        ui.p(
                            "This panel shows the labels or category identifiers present in the dataset."
                        ),
                        ui.tags.ul(
                            ui.tags.li(
                                "Each label represents a class or group associated with your data."
                            ),
                            ui.tags.li(
                                "Useful for supervised tasks like classification or evaluation."
                            ),
                            ui.tags.li(
                                "Check for consistency in labels across dataset versions."
                            ),
                        ),
                        ui.p(
                            {"class": "text-muted small"},
                            "Ensure all expected labels are present before modeling.",
                        ),
                    ),
                ),
                ui.column(
                    9,
                    ui.card(
                        ui.div(
                            {"style": "overflow-x: auto"},
                            ui.output_ui("labels_plot_ui"),
                        )
                    ),
                ),
            ),
        )
    )


@module.server
def labels_server(input, output, session):
    plot_state = reactive.Value({"success": True, "error": None, "plot": None})

    @reactive.Calc
    def labels_plot():
        user_table = shared_first_choice.get()

        if not user_table:
            return {"success": False, "error": "No dataset selected.", "plot": None}

        try:
            plot_obj = plot_LabelMatrix(table=user_table)
            return {"success": True, "plot": plot_obj, "error": None}
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating plot for '{user_table}': {str(e)}",
                "plot": None,
            }

    @reactive.Effect
    def update_state():
        plot_state.set(labels_plot())

    @output
    @render.ui
    def labels_plot_ui():
        result = plot_state.get()
        if result["success"] and isinstance(result["plot"], ggplot):
            return ui.div(
                # The output_plot ID here must be unique and matched by the render.plot below
                ui.output_plot("label_matrix_plot", width="100%", height="600px")
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
    @render.plot(alt="Label Matrix")
    def label_matrix_plot():
        result = plot_state.get()
        return result["plot"] if result["success"] else None
