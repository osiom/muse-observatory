from typing import Dict, List

import base64
from nicegui import ui

from sidebar import create_sidebar
from config.observatory_css import get_logo_css, get_cosmic_css, get_text_css, get_load_cosmic_css
from models.muse import Oracle
from utils.media import get_base64_comet
from utils.projects import get_project_response

from logger import get_logger

logger = get_logger(__name__)


def apply_styles(color: str, support_color: str, astro_color: str):
    """Integrated styles combining styles.py with terminal effects and cosmic enhancements"""
    logo_css = get_logo_css()
    ui.add_head_html(logo_css)

    # 1. Base cosmic styles from styles.py
    cosmic_css, stars = get_cosmic_css(color, support_color, astro_color)
    ui.add_head_html(cosmic_css)
    ui.add_body_html(stars)
    text_style = get_text_css(color)
    ui.add_head_html(text_style)
    #sidebar = create_sidebar(color, astro_color)
    #sidebar.render()

def show_projects_dialog(projects: List[Dict], muse_name: str, muse_color: str) -> bool:
    """Display projects in a dialog with muse-themed styling"""
    dialog = ui.dialog().classes("w-full max-w-lg")
    with dialog, ui.card().classes("w-full p-0 overflow-hidden"):
        ui.html(f'''
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
        ''')
        
        # Center everything with flex and items-center
        with ui.column().classes("w-full p-4 gap-3 relative items-center"):
            # Header with muse reference - already centered
            ui.html(f'''
                <div class="text-2xl font-bold text-center text-black" 
                     style="text-shadow: 0 1px 2px rgba(0,0,0,0.2); line-height: 1.3;">
                    Guided by inspiration,<br>
                    <span style="color: {muse_color};">{muse_name}</span> connects you to these projects
                </div>
            ''')
            
            # Projects list container - center the cards themselves
            with ui.column().classes("w-full gap-3 items-center"):
                for project in projects:
                    with ui.card().classes("w-full p-3 bg-white bg-opacity-90 border-l-4 mx-auto").style(
                        f"border-left-color: {muse_color}"
                    ):
                        # Center all content within each card
                        with ui.column().classes("gap-2 items-center justify-center text-center w-full"):
                            ui.label(project['project_name']).classes("text-lg font-semibold text-black")
                            ui.label(f"by {project['organization']}").classes("text-md text-gray-800")
                            ui.label(f"Scope: {project['geographic_level']}").classes("text-sm text-gray-600")
                            # Center the link row
                            with ui.row().classes("items-center justify-center gap-2"):
                                ui.icon("link", color="primary")
                                ui.link("Visit", project['link_to_organization'], new_tab=True).classes("text-primary")
            
            # Close button - already full width and centered
            ui.button(
                "Close", 
                on_click=dialog.close
            ).classes("dialog-button w-full mt-4")
    return dialog

async def handle_share(oracle_day: Oracle, user_input: str, share_button: ui.button):
    """Handle the share button click with cosmic starry loader"""
    # Create cosmic loader with transparent background
    with ui.column().classes("fixed inset-0 items-center justify-center bg-black bg-opacity-30") as loader:
        loader.style("z-index: 9999; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;")
        
        # Loading message with higher z-index than stars
        with ui.column().classes(f"relative z-50 bg-{oracle_day.astro_color} bg-opacity-70 p-8 rounded-xl"):
            ui.label("Capting signals... 📡").classes("text-3xl font-bold text-white mb-4")
        
        # Add HTML/CSS for animated cosmic background
        loader_cosmic_css = get_text_css(oracle_day.color)
        ui.add_head_html(loader_cosmic_css)
        
        # Container for cosmic elements with proper positioning
        cosmic_container = ui.element('div')
        cosmic_container.classes('cosmic-loader')
        cosmic_loader_css, stars = get_load_cosmic_css(oracle_day.color)
        ui.html(cosmic_loader_css)
        ui.html(stars)

    try:
        # Get project recommendations
        projects_data = await get_project_response(oracle_day, user_input)
        if not projects_data or not projects_data.get('projects'):
            ui.notify("No cosmic connections found today", type='info')
            projects_data = {'projects': []}

        # Remove share button
        share_button.delete()
        
        # Show projects dialog
        dialog = show_projects_dialog(
            projects_data['projects'],
            oracle_day.muse_name,
            oracle_day.color
        )
        dialog.open()
        # Save to database
        oracle_day.save_inspiration(user_input, projects_data['projects'])
        ui.notify(f"Shared with the {oracle_day.muse_name}!", type='positive')
    except Exception as e:
        ui.notify(f"Sandstorm turbulences!: {str(e)}", type='negative')
        logger.error(f"Share error: {str(e)}")
    finally:
        loader.delete()

@ui.page('/observatory')
def  observatory():
    oracle_day = Oracle()
    apply_styles(oracle_day.color, oracle_day.support_color ,oracle_day.astro_color)
    
    with ui.column().classes("main-container"):
        # Background elements first
        ui.html('<div class="cosmic-overlay"></div>')
        ui.html('<div class="static-overlay"></div>')
        
        # Content with forced center alignment
        with ui.column().classes("w-full text-center"):
            # Logo and headers
            with open("static/logo.png", "rb") as img_file:
                logo_base64 = base64.b64encode(img_file.read()).decode()
                ui.html(f'''
                <div class="logo-container">
                    <a href="https://cocoex.xyz" target="_blank">
                        <img src="data:image/png;base64,{logo_base64}" class="logo-img">
                    </a>
                </div>
                ''')
                        
            # Text elements with center alignment
            ui.label("Today's Muse").classes("muse-subtitle").style('margin-top: 7px')
            ui.label(oracle_day.muse_name.upper()).classes("muse-title text-center")
            ui.label(f"for {oracle_day.social_cause}").classes("muse-subtitle text-center")
            
            # Terminal-style elements
            ui.label(oracle_day.fun_fact).classes("fun-fact text-center")
            ui.link("Source", oracle_day.fact_check_link).classes("source-link text-center")
            
            # Question and input
            ui.label(oracle_day.question_asked).classes("question-text text-center")
            
            with ui.column().classes("input-container w-full mx-auto"):
                user_input = ui.textarea(placeholder="Share your inspiration...") \
                    .classes("clean-input mx-auto")
                
            async def on_share_click():
                if not user_input.value.strip():
                    ui.notify(f"Please inspire {oracle_day.muse_name}!", type='warning')
                    return
                # Call the async handle_share function
                await handle_share(oracle_day, user_input.value, share_button)

            share_button = ui.button(
                f"SHARE WITH {oracle_day.muse_name.upper()}",
                on_click=on_share_click
            ).classes("muse-button mx-auto")
