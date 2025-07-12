from nicegui import ui


class HelpButton:
    def __init__(self: "HelpButton", color: str = "black"):
        self.color = color
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
                        margin-bottom: 0.5rem;
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
                        font-size: 0.85rem;
                    ">
                        <p style="margin-bottom: 0.75rem;">
                            Welcome to Muse Observatory! Each day brings a new <strong>Muse</strong> with unique energy and theme.
                        </p>

                        <p style="margin-bottom: 0.75rem;">
                            <strong>🌌 How it works:</strong><br>
                            • Get inspired with a fun-fact<br>
                            • Share your thoughts with the Muse<br>
                            • Discover matching real-world projects
                        </p>

                        <p style="margin-bottom: 0.75rem;">
                            <strong>🌟 Building together:</strong><br>
                            Projects are added to our constellation, creating a shared resource for future collaborations.
                        </p>

                        <p style="margin-bottom: 0.5rem; font-style: italic; color: rgba(255,255,255,0.7); font-size: 0.8rem;">
                            ☁️ Self-hosted experience — no clouds in our cosmo :)
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
        """Render the help button as simple text in the top left corner"""
        help_button = (
            ui.button("?", on_click=self.instructions_dialog.open)
            .classes("fixed top-4 left-4 z-50")
            .style(
                "background: transparent !important; "
                f"color: {self.color}; "
                "border: none !important; "
                "box-shadow: none !important; "
                "font-size: 24px; "
                "font-weight: bold; "
                "padding: 8px; "
                "min-width: auto; "
                "width: auto; "
                "height: auto; "
                "cursor: pointer; "
                "transition: opacity 0.3s ease;"
                "z-index: 9999 !important; "
            )
        )

        # Add simple hover effect and remove any default button styling
        ui.add_head_html(
            """
            <style>
        .fixed.top-4.left-4.z-50 {{
            z-index: 9999 !important;
            position: fixed !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .fixed.top-4.left-4.z-50:hover {{
            opacity: 0.7 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}
        </style>
        """
        )


# Factory function for easy use
def create_help_button(color: str = "white") -> HelpButton:
    return HelpButton(color)
