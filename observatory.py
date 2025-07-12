import base64
from typing import Dict, List

from fastapi import Request
from nicegui import ui

from css.observatory_css import get_cosmic_css, get_load_cosmic_css, get_text_css
from models.helper import create_help_button
from models.muse import Oracle
from utils.generate_projects import get_project_response
from utils.limiter import limiter
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
    """Display projects in a mobile-optimized dialog with muse-themed styling"""
    logger.info(
        f"🌌 Opening projects dialog for muse '{muse_name}' with {len(projects)} cosmic projects."
    )

    dialog = ui.dialog().classes("w-full h-full flex items-center justify-center p-4")

    with dialog:
        # Main container with margins for background visibility
        with ui.card().classes("w-full max-w-sm mx-4 max-h-[85vh] overflow-hidden"):
            # Background overlay
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

            with ui.column().classes("w-full p-3 gap-2 relative"):
                # Compact header for mobile
                ui.html(
                    f"""
                    <div class="text-base font-bold text-center text-black mb-1"
                         style="text-shadow: 0 1px 2px rgba(0,0,0,0.2); line-height: 1.1;">
                        <span style="color: {muse_color};">{muse_name}</span> Projects
                    </div>
                    """
                )

                # Compact projects container
                with ui.column().classes("w-full gap-2"):
                    for project in projects:
                        logger.info(
                            f"🚀 Displaying project: {project['project_name']} (by {project['organization']})"
                        )

                        with ui.card().classes(
                            "w-full p-2 bg-white bg-opacity-90 border-l-2"
                        ).style(f"border-left-color: {muse_color}"):
                            with ui.column().classes("w-full gap-1"):
                                # Project name - very compact
                                ui.label(project["project_name"]).classes(
                                    "text-sm font-semibold text-black leading-tight"
                                ).style(
                                    "word-wrap: break-word; max-height: 2.5em; overflow: hidden;"
                                )

                                # Organization - smaller text
                                ui.label(f"by {project['organization']}").classes(
                                    "text-xs text-gray-700"
                                ).style(
                                    "word-wrap: break-word; max-height: 1.2em; overflow: hidden;"
                                )

                                # Compact info row
                                with ui.row().classes(
                                    "items-center justify-between gap-2"
                                ):
                                    ui.label(f"{project['geographic_level']}").classes(
                                        "text-xs text-gray-600"
                                    )

                                    # Compact link
                                    with ui.row().classes("items-center gap-1"):
                                        ui.icon("link", size="xs").classes(
                                            "text-primary"
                                        )
                                        ui.link(
                                            "Visit",
                                            project["link_to_organization"],
                                            new_tab=True,
                                        ).classes("text-primary text-xs")

                    # Close button with muse color
                    ui.button("Close", on_click=dialog.close).classes(
                        "dialog-button w-full mt-2"
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
        logger.info(f"🌌 Inspiration shared with {oracle_day.muse_name}!")
        ui.notify(f"Shared with {oracle_day.muse_name}!", type="positive")
    except Exception as e:
        logger.error(f"☄️ Sandstorm turbulence during share: {str(e)}")
        ui.notify(f"Sandstorm turbulences!: {str(e)}", type="negative")
    finally:
        loader.delete()


@ui.page("/observatory")
@limiter.limit("10/minute")
def observatory(request: Request):
    logger.info("🛰️ Rendering the Observatory page — aligning the cosmic interface...")
    oracle_day = Oracle()
    apply_styles(oracle_day.color, oracle_day.support_color, oracle_day.astro_color)

    # Create and render help button instead of sidebar
    help_button = create_help_button(oracle_day.color)

    with ui.column().classes("main-container"):
        # Background elements first
        ui.html('<div class="cosmic-overlay"></div>')
        ui.html('<div class="static-overlay"></div>')

        # Content with forced center alignment and minimal spacing
        with ui.column().classes("w-full text-center").style("padding-top: 0px;"):
            # Logo and headers - centered alignment with reduced spacing
            with ui.row().classes("w-full justify-center"):
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
            # Text elements with minimal spacing
            ui.label("Today's Muse").classes("muse-subtitle text-center").style(
                "margin-top: 0px; margin-bottom: 0px;"
            )
            ui.label(oracle_day.muse_name.upper()).classes(
                "muse-title text-center"
            ).style("margin-top: 0px; margin-bottom: 0px;")
            ui.label(f"for {oracle_day.social_cause}").classes(
                "muse-subtitle text-center"
            ).style("margin-top: 0px; margin-bottom: 2px;")

            # Terminal-style elements
            ui.label(oracle_day.fun_fact).classes("fun-fact text-center").style(
                "margin-top: 0px; margin-bottom: 2px;"
            )
            ui.link("Source", oracle_day.fact_check_link).classes(
                "source-link text-center"
            ).style("margin-top: 0px; margin-bottom: 4px;")

            # Question and input
            ui.label(oracle_day.question_asked).classes(
                "question-text text-center w-full"  # Add w-full class
            ).style(
                "margin-top: 0px; margin-bottom: 10px; text-align: center !important;"
            )

            with ui.column().classes("input-container w-full mx-auto max-w-2xl"):
                user_input = ui.textarea(
                    placeholder="Share your inspiration..."
                ).classes(
                    "w-full text-sm sm:text-base rounded-2xl border border-white/30 bg-white/70 backdrop-blur-sm "
                    "shadow-[0_6px_18px_rgba(0,0,0,0.20)] transition-all focus:ring-2 focus:ring-purple-400 focus:ring-offset-2"
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

    # Add mobile-responsive CSS with fixed positioning and height constraints
    ui.add_head_html(
        """
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    /* Fix body and html to prevent infinite scrolling */
    html, body {
        height: 100vh !important;
        max-height: 100vh !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        position: relative !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }

    /* Constrain cosmic background elements */
    .cosmic-overlay, .dust-overlay {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
        z-index: -1 !important;
    }

    /* Constrain all cosmic elements */
    .star, .shooting-star, .cosmic-dust, .nebula-particle, .pulsar {
        position: fixed !important;
        max-height: 100vh !important;
        overflow: hidden !important;
    }

    /* Logo container alignment - responsive */
    .logo-container {
        top: 8px;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        z-index: 1000;
        margin-bottom: 0px;
    }
    .logo-img {
        width: 50px;
        height: 50px;
        object-fit: contain;
    }

    /* Main container with proper height constraints and small margins */
    .main-container {
        min-height: 100vh !important;
        /* max-height: 100vh !important; */
        /* height: 100vh !important; */
        width: calc(100% - 1rem) !important;
        max-width: calc(100% - 1rem) !important;
        margin: 0 0.5rem !important;
        padding: 0.5rem !important;
        padding-top: 0 !important;  /* Remove top padding */
        overflow-y: auto !important;
        overflow-x: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;  /* Start from top */
        box-sizing: border-box !important;
    }

    @media (max-width: 430px) {
        .muse-title {
            font-size: 36px !important;  /* Reduce title size on mobile */
        }

        .muse-subtitle {
            font-size: 16px !important;  /* Reduce subtitle size on mobile */
        }

        .fun-fact, .question-text {
            font-size: 14px !important;  /* Reduce text size on mobile */
            line-height: 1.3 !important;
        }
        .main-container {
            justify-content: flex-start !important;
            width: calc(100% - 0.75rem) !important;
            max-width: calc(100% - 0.75rem) !important;
            margin: 0 0.375rem !important;
            padding: 0.25rem !important;
            padding-top: 0 !important;  /* Start from very top */
            padding-bottom: 10px !important;
        }

        /* Adjust logo position to account for no top padding */
        .logo-container {
            top: 5px !important;  /* Reduced from 8px */
            margin-bottom: 5px !important;
        }
    }

    @media (max-width: 375px) {
        /* iPhone 13 mini specific */
        .main-container {
            justify-content: flex-start !important;
            width: calc(100% - 0.5rem) !important;
            max-width: calc(100% - 0.5rem) !important;
            margin: 0 0.25rem !important;
            padding: 0.25rem !important;
            padding-top: 0 !important;  /* Start from very top */
            padding-bottom: 8px !important;
        }

        /* Adjust logo position */
        .logo-container {
            top: 3px !important;  /* Very close to top */
            margin-bottom: 3px !important;
        }
    }

    /* Ensure all text elements are properly centered with minimal spacing */
    .muse-subtitle, .muse-title, .fun-fact, .source-link, .question-text {
        text-align: center !important;
        display: block !important;
        width: 100% !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }

    /* Minimize spacing between UI elements */
    .main-container > * {
        margin-top: 0px !important;
        margin-bottom: 0px !important;
    }

    /* Ensure content fits within viewport */
    * {
        box-sizing: border-box !important;
    }

    /* Mobile-specific input styling */
    @media (max-width: 430px) {
        input, textarea {
            font-size: 16px !important; /* Prevents zoom on iOS */
            -webkit-appearance: none !important;
            border-radius: 12px !important;
        }
    }

    /* Safari-specific fixes */
    @supports (-webkit-touch-callout: none) {
        .main-container {
            -webkit-overflow-scrolling: touch !important;
        }

        /* Additional iOS Safari fixes */
        body {
            position: fixed !important;
            width: 100% !important;
            height: 100% !important;
        }

        .main-container {
            position: relative !important;
            height: 100vh !important;
            overflow-y: scroll !important;
        }
    }
    </style>
    """
    )
