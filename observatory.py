import base64
from typing import Dict, List

from nicegui import ui

from css.observatory_css import get_cosmic_css, get_load_cosmic_css, get_text_css
from models.helper import create_help_button
from models.muse import Oracle
from utils.generate_projects import get_project_response
from utils.logger import get_logger
from utils.utils import validate_project_input

logger = get_logger(__name__)

logger.info("🪐 Observatory module loaded — ready to chart the cosmic canvas!")


def apply_styles(color: str, support_color: str, astro_color: str):
    """Integrated styles combining styles.py with terminal effects and cosmic enhancements"""
    logger.info(
        f"🌈 Applying cosmic styles: primary={color}, support={support_color}, astro={astro_color}"
    )
    # 1. Base cosmic styles from styles.py
    cosmic_css, stars = get_cosmic_css(color, support_color, astro_color)
    ui.add_head_html(cosmic_css)
    ui.add_body_html(stars)
    text_style = get_text_css(color)
    ui.add_head_html(text_style)


def show_projects_dialog(projects: List[Dict], muse_name: str, muse_color: str) -> bool:
    """Display projects in a dialog with muse-themed styling"""
    logger.info(
        f"🌌 Opening projects dialog for muse '{muse_name}' with {len(projects)} cosmic projects."
    )
    dialog = ui.dialog().classes("w-full max-w-lg")
    with dialog, ui.card().classes("w-full p-0 overflow-hidden"):
        ui.html(
            """
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-size: cover;
                opacity: 0.2;
                z-index: -1;
            "></div>
        """
        )

        # Center everything with flex and items-center
        with ui.column().classes("w-full p-4 gap-3 relative items-center"):
            # Header with muse reference - already centered
            ui.html(
                f"""
                <div class="text-2xl font-bold text-center text-black"
                     style="text-shadow: 0 1px 2px rgba(0,0,0,0.2); line-height: 1.3;">
                    Guided by inspiration,<br>
                    <span style="color: {muse_color};">{muse_name}</span> connects you to these projects
                </div>
            """
            )

            # Projects list container - center the cards themselves
            with ui.column().classes("w-full gap-3 items-center"):
                for project in projects:
                    logger.info(
                        f"🚀 Displaying project: {project['project_name']} (by {project['organization']})"
                    )
                    with ui.card().classes(
                        "w-full p-3 bg-white bg-opacity-90 border-l-4 mx-auto"
                    ).style(f"border-left-color: {muse_color}"):
                        # Center all content within each card
                        with ui.column().classes(
                            "gap-2 items-center justify-center text-center w-full"
                        ):
                            ui.label(project["project_name"]).classes(
                                "text-lg font-semibold text-black"
                            )
                            ui.label(f"by {project['organization']}").classes(
                                "text-md text-gray-800"
                            )
                            ui.label(f"Scope: {project['geographic_level']}").classes(
                                "text-sm text-gray-600"
                            )
                            # Center the link row
                            with ui.row().classes("items-center justify-center gap-2"):
                                ui.icon("link", color="primary")
                                ui.link(
                                    "Visit",
                                    project["link_to_organization"],
                                    new_tab=True,
                                ).classes("text-primary")

            # Close button - already full width and centered
            ui.button("Close", on_click=dialog.close).classes(
                "dialog-button w-full mt-4"
            )
    return dialog


async def handle_share(oracle_day: Oracle, user_input: str, share_button: ui.button):
    """Handle the share button click with cosmic starry loader"""
    logger.info(
        f"✨ User is sharing inspiration with muse '{oracle_day.muse_name}'. Input: '{user_input[:60]}...'"
    )
    # Create cosmic loader with transparent background
    with ui.column().classes(
        "fixed inset-0 items-center justify-center bg-black bg-opacity-30"
    ) as loader:
        loader.style(
            "z-index: 9999; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;"
        )

        # Loading message with higher z-index than stars
        with ui.column().classes(
            f"relative z-50 bg-{oracle_day.astro_color} bg-opacity-70 p-8 rounded-xl"
        ):
            ui.label("Capting signals... 📡").classes(
                "text-3xl font-bold text-white mb-4"
            )

        # Add HTML/CSS for animated cosmic background
        loader_cosmic_css = get_text_css(oracle_day.color)
        ui.add_head_html(loader_cosmic_css)

        # Container for cosmic elements with proper positioning
        cosmic_container = ui.element("div")
        cosmic_container.classes("cosmic-loader")
        cosmic_loader_css, stars = get_load_cosmic_css(oracle_day.color)
        ui.html(cosmic_loader_css)
        ui.html(stars)

    try:
        # Get project recommendations
        logger.info("🔭 Querying cosmic engine for project recommendations...")
        projects_data = await get_project_response(oracle_day, user_input)
        if not projects_data or not projects_data.get("projects"):
            logger.warning("🌑 No cosmic connections found for this inspiration.")
            ui.notify("No cosmic connections found today", type="info")
            projects_data = {"projects": []}
        else:
            logger.info(f"🌠 {len(projects_data['projects'])} cosmic projects found!")
        # Remove share button
        share_button.delete()
        # Show projects dialog
        dialog = show_projects_dialog(
            projects_data["projects"], oracle_day.muse_name, oracle_day.color
        )
        dialog.open()
        # Save to database
        logger.info("📝 Saving inspiration and cosmic projects to the ledger...")
        oracle_day.save_inspiration(user_input, projects_data["projects"])
        logger.info(f"🌌 Inspiration shared with the {oracle_day.muse_name}!")
        ui.notify(f"Shared with the {oracle_day.muse_name}!", type="positive")
    except Exception as e:
        logger.error(f"☄️ Sandstorm turbulence during share: {str(e)}")
        ui.notify(f"Sandstorm turbulences!: {str(e)}", type="negative")
    finally:
        loader.delete()


@ui.page("/observatory")
def observatory():
    logger.info("🛰️ Rendering the Observatory page — aligning the cosmic interface...")
    oracle_day = Oracle()
    apply_styles(oracle_day.color, oracle_day.support_color, oracle_day.astro_color)

    # Create and render help button instead of sidebar
    help_button = create_help_button(oracle_day.color)

    with ui.column().classes("main-container"):
        # Background elements first
        ui.html('<div class="cosmic-overlay"></div>')
        ui.html('<div class="static-overlay"></div>')

        # Content with forced center alignment and normal spacing
        with ui.column().classes("w-full text-center").style("padding-top: 20px;"):
            # Logo and headers - centered alignment
            with ui.row().classes("w-full justify-center mb-4"):
                with open("img/logo.png", "rb") as img_file:
                    logo_base64 = base64.b64encode(img_file.read()).decode()
                    ui.html(
                        f"""
                    <div class="logo-container" style="display: flex; justify-content: center; align-items: center;">
                        <a href="https://cocoex.xyz" target="_blank">
                            <img src="data:image/png;base64,{logo_base64}" class="logo-img">
                        </a>
                    </div>
                    """
                    )
            help_button.render()
            # Text elements with proper spacing and center alignment
            ui.label("Today's Muse").classes("muse-subtitle text-center").style(
                "margin-top: 10px; margin-bottom: 5px;"
            )
            ui.label(oracle_day.muse_name.upper()).classes(
                "muse-title text-center"
            ).style("margin-bottom: 5px;")
            ui.label(f"for {oracle_day.social_cause}").classes(
                "muse-subtitle text-center"
            ).style("margin-bottom: 20px;")

            # Terminal-style elements
            ui.label(oracle_day.fun_fact).classes("fun-fact text-center").style(
                "margin-bottom: 10px;"
            )
            ui.link("Source", oracle_day.fact_check_link).classes(
                "source-link text-center"
            ).style("margin-bottom: 30px;")

            # Question and input
            ui.label(oracle_day.question_asked).classes(
                "question-text text-center"
            ).style("margin-bottom: 20px;")

            with ui.column().classes("input-container w-full mx-auto max-w-2xl"):
                user_input = (
                    ui.textarea(placeholder="Share your inspiration...")
                    .classes(
                        "w-full text-base rounded-2xl border border-white/30 bg-white/70 backdrop-blur-sm "
                        "shadow-[0_6px_18px_rgba(0,0,0,0.20)] transition-all focus:ring-2 focus:ring-purple-400 focus:ring-offset-2"
                    )
                    .style("padding: 1rem; resize: vertical;")
                )

            async def on_share_click():
                validated_input = validate_project_input(user_input.value.strip())
                if validated_input is None:
                    logger.info("User input validation failed.")
                    ui.notify(f"Please inspire {oracle_day.muse_name}!", type="warning")
                    return
                # Call the async handle_share function
                await handle_share(oracle_day, validated_input, share_button)

            share_button = ui.button(
                f"SHARE WITH {oracle_day.muse_name.upper()}", on_click=on_share_click
            ).classes("muse-button mx-auto")

    # Add minimal CSS for proper alignment
    ui.add_head_html(
        """
    <style>
    /* Logo container alignment */
    .logo-container {
        position: fixed;
        top: 20px;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        z-index: 1000;
    }
    .logo-img {
            width: 60px;
            height: 60px;
            object-fit: contain;
    }
    /* Ensure all text elements are properly centered */
    .muse-subtitle, .muse-title, .fun-fact, .source-link, .question-text {
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }
    </style>
    """
    )

    # Optionally, you can add per-user or per-IP rate limiting to actions here if you expose any API endpoints from this file in the future.
    # For now, main API endpoints are protected in app.py.
