from nicegui import ui


class HelpButton:
    def __init__(self: "HelpButton", color: str = "black", auto_open: bool = False):
        self.color = color
        self.auto_open = auto_open
        self.instructions_dialog = None
        self.create_dialog()

    def create_dialog(self: "HelpButton"):
        self.instructions_dialog = ui.dialog()
        with self.instructions_dialog:
            with ui.card().classes("max-w-sm p-3").style(  # Smaller card, less padding
                "background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(20,20,40,0.9)); "
                "color: white; "
                "border: 1px solid rgba(255,255,255,0.2); "
                "border-radius: 16px; "
                "backdrop-filter: blur(15px); "
                "max-height: 85vh; "  # Constrain to screen height
                "overflow-y: auto;"
            ):
                # Compact header
                ui.html(
                    f"""
                    <div style="
                        text-align: center;
                        margin-bottom: -0.25rem;
                        color: {self.color};
                        text-shadow: 0 0 10px rgba(255,255,255,0.3);
                    ">
                        <h2 style="font-size: 1.2rem; font-weight: bold; margin: 0;">
                            🔭 Observatory Instructions
                        </h2>
                    </div>
                """
                )

                # Condensed instructions
                ui.html(
                    """
                    <div style="
                        line-height: 1.4;
                        color: rgba(255,255,255,0.9);
                        text-align: left;
                        font-size: 0.95rem;
                        font-style: normal;
                        margin-top: 0;
                        padding-top: 0;
                    ">
                        <p style="margin-top: 0; margin-bottom: 0.75rem;">
                            Welcome to Muse Observatory! Each day introduces a new <strong>Muse</strong> with its own unique energy and theme. These Muses are narratives built on top of the <a href="https://cocoex.xyz" target="_blank" rel="noopener noreferrer">cocoex comet-collab</a>. Each Muse is connected to a specific <a href="https://sdgs.un.org/goals" target="_blank" rel="noopener noreferrer">Sustainable Development Goal (SDG)</a> and a related social cause.
                        </p>
                        <p style="margin-bottom: 0.75rem; font-style: normal;">
                            <strong>🌌 How it works:</strong><br>
                            • Get inspired by a fun fact about an organism from the kingdoms of life, showing how nature can spark ideas and synergies for real-world human applications.<br>
                            • Share your thoughts and reflections about what the Muse of the day inspired in you.<br>
                            • Once inspired, the Muse will connect you with real-world projects or NGOs aligned with your vision — because we're never alone in this journey!
                        </p>
                        <p style="margin-bottom: 0.75rem; font-style: normal;">
                            <strong>🌟 Building together:</strong><br>
                            Finally, every inspiration and project discovered will be added to the <a href="https://cocoex.xyz" target="_blank" rel="noopener noreferrer">cocoex register</a>, helping us build a collective database of initiatives and ideas — from the people, for the people. :)
                        </p>
                    </div>
                """
                )

                # Compact close button
                ui.button("Got it!", on_click=self.instructions_dialog.close).classes(
                    "muse-button mx-auto mt-2"
                ).style(
                    "min-width: 100px; "
                    "background: linear-gradient(135deg, rgba(100, 70, 255, 0.8), rgba(180, 80, 255, 0.8)); "
                    "border: 1px solid rgba(255, 255, 255, 0.2) !important; "
                    "border-radius: 12px !important; "
                    "padding: 6px 12px !important; "
                    "font-weight: 500 !important; "
                    "font-size: 0.85rem !important; "
                    "display: flex; "
                    "align-items: center; "
                    "justify-content: center; "
                    "transition: all 0.3s ease !important; "
                )

    def render(self: "HelpButton"):
        """Render the help button as a circular button with white question mark"""
        help_button = (
            ui.button("?", on_click=self.instructions_dialog.open)
            .classes("fixed top-4 left-4 z-50")
            .style(
                f"background: {self.color} !important; "
                "color: white !important; "
                "border: none !important; "
                "border-radius: 50% !important; "
                "box-shadow: 0 2px 8px rgba(0,0,0,0.4), 0 0 2px rgba(255,255,255,0.3) !important; "
                "font-size: 18px; "
                "font-weight: bold; "
                "padding: 0; "
                "min-width: 30px; "
                "width: 30px; "
                "height: 30px; "
                "display: flex; "
                "align-items: center; "
                "justify-content: center; "
                "cursor: pointer; "
                "transition: transform 0.3s ease, box-shadow 0.3s ease;"
                "z-index: 9999 !important; "
            )
        )

        # Add hover effect and ensure consistent styling
        ui.add_head_html(
            """
            <style>
        .fixed.top-4.left-4.z-50 {
            z-index: 9999 !important;
            position: fixed !important;
        }

        .fixed.top-4.left-4.z-50:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4), 0 0 4px rgba(255,255,255,0.5) !important;
        }
        </style>
        """
        )

        # Auto-open dialog if enabled
        if self.auto_open:
            ui.timer(0.5, lambda: self.instructions_dialog.open(), once=True)


# Factory function for easy use
def create_help_button(color: str = "white", auto_open: bool = False) -> HelpButton:
    return HelpButton(color, auto_open)
