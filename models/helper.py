from nicegui import ui


class HelpButton:
    def __init__(self: "HelpButton", color: str = "black"):
        self.color = color
        self.instructions_dialog = None
        self.create_dialog()

    def create_dialog(self: "HelpButton"):
        """Create the instructions dialog with cosmic styling"""
        self.instructions_dialog = ui.dialog()
        with self.instructions_dialog:
            with ui.card().classes("max-w-lg p-6").style(
                "background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(20,20,40,0.9)); "
                "color: white; "
                "border: 1px solid rgba(255,255,255,0.2); "
                "border-radius: 16px; "
                "backdrop-filter: blur(15px);"
            ):
                # Header with minimal spacing
                ui.html(
                    f"""
                    <div style="
                        text-align: center;
                        margin-bottom: 0.5rem;
                        color: {self.color};
                        text-shadow: 0 0 10px rgba(255,255,255,0.3);
                    ">
                        <h2 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0;">
                            🔭 Instructions
                        </h2>
                """
                )

                # Instructions content (tight spacing)
                ui.html(
                    """
                    <div style="
                        line-height: 1.3;
                        color: rgba(255,255,255,0.9);
                        text-align: justify;
                        font-size: 1.1rem;
                        margin-top: 0.5rem;
                    ">
                        <h4 style="color: white; font-size: 1.3rem; font-weight: normal; margin: 0.25rem 0 0.75rem 0;">
                            Welcome to the Muse Observatory!
                        </h4>
                        <p style="margin-bottom: 1rem;">
                            Your telescope into the universe of cocoex — where every day, a new Muse appears to guide your journey.
                        </p>

                        <h4 style="color: white; font-size: 1.15rem; font-weight: normal; margin: 0.75rem 0 0.5rem 0;">
                            🌌 How It Works
                        </h4>
                        <p style="margin-bottom: 1rem;">
                            Each day reveals a <strong>Muse</strong> — a unique guide with its own energy, color, and theme. You'll also receive a <strong>fun fact</strong> to spark your curiosity.
                        </p>
                        <p style="margin-bottom: 1rem;">
                            You'll get an <strong>inspiring question</strong>. When you answer, the Observatory shows real-world projects connected to your Muse's synergy.
                        </p>

                        <h4 style="color: white; font-size: 1.15rem; font-weight: normal; margin: 0.75rem 0 0.5rem 0;">
                            🛰️ What Happens Next
                        </h4>
                        <p style="margin-bottom: 1rem;">
                            Your answer becomes a <strong>star</strong> in the Observatory's sky, joining others in this creative constellation.
                        </p>
                        <p style="margin-bottom: 1rem;">
                            You'll see projects matching your Muse's theme to explore or join.
                        </p>

                        <h4 style="color: white; font-size: 1.15rem; font-weight: normal; margin: 0.75rem 0 0.5rem 0;">
                            🔭 Why Explore?
                        </h4>
                        <p style="margin-bottom: 1rem;">
                            The Observatory is a growing map of creativity and shared discovery. Your thoughts become part of this living collection.
                        </p>
                        <p style="margin-bottom: 1rem;">
                            Together, these form the <strong>stardust</strong> for future collaborations — a shared resource of ideas within cocoex.
                        </p>

                        <p style="margin-bottom: 1rem; font-style: italic; color: rgba(255,255,255,0.7);">
                            <small>☁️ A self-hosted experience — no clouds in our cosmo :)</small>
                        </p>
                    </div>
                """
                )

                # Close button (original cosmic style but wider)
                ui.button("Close!", on_click=self.instructions_dialog.close).classes(
                    "muse-button mx-auto mt-2"
                ).style(
                    "min-width: 140px; "  # Wider to prevent text cutoff
                    "background: linear-gradient(135deg, rgba(100, 70, 255, 0.8), rgba(180, 80, 255, 0.8)); "
                    "border: 1px solid rgba(255, 255, 255, 0.2) !important; "
                    "border-radius: 12px !important; "
                    "padding: 12px 16px !important; "
                    "font-weight: 500 !important; "
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
