from shiny import module, render, ui, reactive
import emoji
from htmltools import HTML, TagList
from spectredash.getgit import get_diff, visualize_diff
from spectredash.utils import shared_first_choice



@module.ui
def diff_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.div(
                {"class": "d-flex justify-content-between align-items-center mb-3"},
                ui.h2(
                    f"{emoji.emojize(':magnifying_glass_tilted_left:')} Git Diff",
                    class_="m-0"
                ),
                ui.input_action_button(
                    "fetch_diff",
                    "Fetch",
                    class_="btn btn-sm btn-outline-primary ms-3"  # add left margin (Bootstrap `ms-3`)
                )
            ),
            ui.output_ui("diff_or_message")
        )
    )






@module.server
def diff_server(input, output, session):

    render_state = reactive.Value({"valid": True, "error": None})
    diff_lines_val = reactive.Value([])

    # Observe button clicks using reactive.event
    @reactive.Effect
    @reactive.event(input.fetch_diff)  # Only trigger when the button is clicked
    def _():
        try:
            table_value = shared_first_choice.get()
            lines = get_diff(table=table_value)
            diff_lines_val.set(lines)
            render_state.set({"valid": True, "error": None})
        except Exception as e:
            render_state.set({"valid": False, "error": f"Failed to get diff: {str(e)}"})
            diff_lines_val.set([])

    @reactive.Calc
    def diff_html_content():
        lines = diff_lines_val.get()
        if not lines:
            return None
        try:
            html = visualize_diff(lines, browse=False)
            return HTML(html)
        except Exception as e:
            render_state.set({"valid": False, "error": f"Failed to render diff: {str(e)}"})
            return None

    @output
    @render.ui
    def diff_or_message():
        state = render_state.get()

        if not state["valid"]:
            return ui.div(
                {"class": "d-flex flex-column justify-content-center align-items-center",
                 "style": "height: 600px; background-color: #f8f9fa;"},
                ui.tags.i({"class": "fa fa-exclamation-circle text-warning fa-4x mb-3"}),
                ui.h4("Diff Error", class_="text-danger"),
                ui.p(ui.HTML(state["error"]), class_="text-center text-muted"),
                ui.p("Please check your GitLab connection or table name.", class_="text-center")
            )

        if not diff_lines_val.get():
            return ui.p("Click 'Fetch' to load the latest diff.")

        html_content = diff_html_content()
        if html_content is None:
            return ui.p("No diff available.")

        return html_content




