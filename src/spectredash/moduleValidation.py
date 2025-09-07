# moduleValidation.py


from shiny import module, reactive, render, ui
import os
import emoji

from spectredash.getduck import duckdb_table

from spectredash.utils import shared_first_choice, shared_second_choice


@module.ui
def validation_ui():
    return ui.navset_card_underline(
        ui.nav_panel(
            ui.h4(
                f"{emoji.emojize(':fire_extinguisher:')} Validation Report",
                class_="m-0",
            ),
            ui.row(
                ui.column(
                    3,
                    ui.card(
                        ui.p(
                            "The validation report provides a detailed summary of all checks performed by Pointblank."
                        ),
                        ui.tags.ul(
                            ui.tags.li(
                                "Each section represents a specific validation step applied to the dataset."
                            ),
                            ui.tags.li(
                                "Results are color-coded to indicate passed, failed, or warning-level checks."
                            ),
                            ui.tags.li(
                                "Use the report to identify issues, verify expectations, and ensure data integrity."
                            ),
                        ),
                        ui.p(
                            {"class": "text-muted small"},
                            "Scroll horizontally or zoom out if the report doesn't fit your screen.",
                        ),
                    ),
                ),
                ui.column(
                    9,
                    ui.card(
                        ui.div(
                            {"style": "overflow-x: auto"},
                            ui.output_ui("validation_report_ui"),
                        )
                    ),
                ),
            ),
        )
    )


@module.server
def validation_server(input, output, session):
    report_state = reactive.Value({"valid": True, "error": None})

    @reactive.Calc
    def validation_report():
        ds = shared_first_choice.get()
        ver = shared_second_choice.get()

        if not ds or not ver:
            return {"success": False, "error": "No dataset or version selected."}

        try:
            pointer_df = duckdb_table(table="pointers")
            pointer_df = pointer_df[pointer_df["table"] == ds]
            pointer_df = pointer_df[pointer_df["version"] == ver]

            if pointer_df.empty:
                return {
                    "success": False,
                    "error": f"No matching report found for dataset '{ds}' and version '{ver}'.",
                }

            # report_path = os.path.join("data", pointer_df.iloc[0]["report_path"])
            report_path = os.path.join(
                "src", "spectredash", "data", pointer_df.iloc[0]["report_path"]
            )

            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return {"success": True, "content": content, "path": report_path}
            else:
                return {
                    "success": False,
                    "error": f"Report file not found: {report_path}",
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error loading validation report: {str(e)}",
            }

    @reactive.Effect
    def update_state():
        result = validation_report()
        report_state.set({"valid": result["success"], "error": result.get("error")})

    @output
    @render.ui
    def validation_report_ui():
        state = report_state.get()

        if state["valid"]:
            return ui.HTML(validation_report()["content"])
        else:
            return ui.div(
                {
                    "class": "d-flex flex-column justify-content-center align-items-center",
                    "style": "min-height: 400px; background-color: #f8f9fa;",
                },
                ui.tags.i(class_="fas fa-exclamation-circle text-warning fa-4x mb-3"),
                ui.h4("Report Not Available", class_="text-danger"),
                ui.p(ui.HTML(state["error"]), class_="text-center text-muted"),
                ui.p(
                    "Please select a different dataset or contact the administrator.",
                    class_="text-center",
                ),
            )

    @output
    @render.download
    def download_report():
        def filename():
            ds = shared_first_choice.get() or "report"
            return f"{ds}_validation_report.html"

        def content(file):
            result = validation_report()
            if result["success"]:
                with open(result["path"], "rb") as fsrc:
                    file.write(fsrc.read())
            else:
                file.write(result["error"].encode("utf-8"))

        return {"filename": filename, "content": content}
