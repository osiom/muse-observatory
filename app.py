import os
import time
import base64
import uuid
import random
import asyncio
import re
from datetime import datetime
from typing import Dict, Any

import psycopg2
from nicegui import app, ui
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from logger import get_logger
from typing import List, Dict, Any

from projects import get_project_response

# Initialize
logger = get_logger(__name__)
os.environ['TZ'] = 'Europe/Berlin'  # Set timezone early in your app
time.tzset()  # Apply the timezone
load_dotenv()

# Muse Color Palette
MUSE_COLORS = {
    "Lunes": "#5783A6",
    "Ares": "#D54D2E",
    "Rabu": "#8CB07F",
    "Thunor": "#F8D86A",
    "Shukra": "#5E47A1",
    "Dosei": "#7F49A2",  # Your purple color for Dosei
    "Solis": "#D48348"
}

# Database config
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "muse_observatory"),
    "user": os.getenv("DB_USER", "museuser"),
    "password": os.getenv("DB_PASSWORD", "musepassword"),
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
}

def get_db_connection():
    """Create a database connection."""
    logger.info("Connecting to the database...")
    return psycopg2.connect(**DB_CONFIG)

def get_base64_gif(gif_path: str) -> str:
    """Convert GIF to base64 with fallback"""
    try:
        with open(gif_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        with open("backgrounds/cocoex.gif", "rb") as f:
            return base64.b64encode(f.read()).decode()

def get_todays_gif() -> str:
    """Get today's GIF path"""
    gif_paths = {
        0: "backgrounds/lunes.gif",
        1: "backgrounds/ares.gif",
        2: "backgrounds/rabu.gif",
        3: "backgrounds/thunor.gif",
        4: "backgrounds/shukra.gif",
        5: "backgrounds/dosei.gif",  # Saturday - Dosei
        6: "backgrounds/solis.gif",
    }
    return gif_paths.get(datetime.now().weekday(), "backgrounds/cocoex.gif")

def apply_styles(muse_name: str):
    """Apply dynamic styles"""
    color = MUSE_COLORS.get(muse_name, "#7F49A2")  # Default to Dosei purple
    
    ui.add_head_html(f'''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');
        
        body {{
            background-image: url("data:image/gif;base64,{get_base64_gif(get_todays_gif())}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            margin: 0;
            font-family: 'Cormorant Garamond', Georgia, serif;
            color: white;
            display: flex;
            justify-content: center;
            min-height: 100vh;
        }}

        .main-container {{
            width: 100%;
            max-width: 900px;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        .muse-title {{
            font-size: 56px;
            font-weight: bold;
            text-align: center;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}
        
        .muse-subtitle {{
            font-size: 32px;
            text-align: center;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}
        
        .fun-fact {{
            font-size: 24px;
            font-style: italic;
            text-align: center;
            line-height: 1.6;
            margin: 0;
            max-width: 800px;
            text-shadow: 0 2px 2px rgba(0,0,0,0.3);
        }}
        
        .input-section {{
            width: 100%;
            max-width: 800px;
            margin: 2rem 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        /* Make the typed text even more visible */
        .nicegui-input {{
            color: #111 !important;
            font-family: 'Cormorant Garamond', Georgia, serif !important;
        }}

        .muse-button {{
            background-color: {color} !important;
            color: white !important;
            font-size: 20px !important;
            font-weight: 600;
            padding: 12px 36px !important;
            border: none !important;
            border-radius: 8px !important;
            cursor: pointer;
            transition: all 0.3s;
            align-items: center;
        }}
        
        .muse-button:hover {{
            opacity: 0.9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .source-link {{
            color: white !important;
            text-decoration: underline;
            font-size: 18px;
        }}
    </style>
    ''')

    ui.add_head_html(f'''
    <style>
        /* QUESTION TEXT - ABOVE INPUT */
        .question-text {{
            font-size: 24px;
            font-style: italic;
            text-align: center;
            margin: 20px auto;
            max-width: 800px;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            line-height: 1.4;
            padding: 0 20px;
        }}

        /* INPUT CONTAINER */
        .input-container {{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0 auto;
        }}

        /* TEXTAREA STYLING */
        .clean-input {{
            width: 65% !important;
            min-height: 100px !important;
            margin: 0 auto !important;
            font-size: 20px !important;
            background: white !important;
            color: black !important;
            border: 2px solid {color} !important;
            border-radius: 12px !important;
            padding: 16px !important;
            font-family: 'Cormorant Garamond' !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        /* PLACEHOLDER TEXT */
        .clean-input::placeholder {{
            color: #666 !important;
            font-style: italic;
            opacity: 1 !important;
        }}

        /* PROMPT TEXT BELOW INPUT */
        .write-prompt {{
            text-align: center;
            color: white;
            font-style: italic;
            margin: 12px;
            font-size: 18px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        }}
         /* CENTERED BUTTON CONTAINER */
        .button-container {{
            display: flex;
            justify-content: center;
            width: 100%;
            margin: 10px;
        }}

        /* BUTTON STYLING */
        .muse-button {{
            background-color: {color} !important;
            color: white !important;
            font-size: 20px !important;
            padding: 12px 36px !important;
            border: none !important;
            border-radius: 8px !important;
            cursor: pointer;
            transition: all 0.3s;
            margin: 0 auto; /* Additional centering */
        }}
    </style>
    ''')

def get_todays_fact() -> Dict[str, Any]:
    """Fetch today's fact"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT * FROM daily_facts WHERE date = %s", (today,))
        return cursor.fetchone() or {
            'muse': 'cocoex',
            'social_cause': 'cocoex',
            'fun_fact': 'The oracle didnt answer today!',
            'question_asked': 'What is the meaning of life?',
            'fact_check_link': '#'
        }
    except Exception as e:
        logger.error(f"Database error: {e}")
        return {
            'muse': 'cocoex',
            'social_cause': 'Database Error',
            'fun_fact': 'Could not fetch fact today',
            'question_asked': 'Try again later?',
            'fact_check_link': '#'
        }
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def save_response(fact_info: Dict[str, Any], user_input: str, projects: List[Dict]):
    """Save both inspiration and projects"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Save inspiration
        cursor.execute("""
            INSERT INTO inspirations 
            (date, id, day_of_week, social_cause, muse, user_inspiration)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """, (
                datetime.now().date(),
                str(uuid.uuid4()),
                datetime.now().strftime('%A'),
                fact_info['social_cause'],
                fact_info['muse'],
                user_input
            ))
        
        inspiration_id = cursor.fetchone()[0]
        
        # Save projects
        for project in projects:
            cursor.execute("""
                INSERT INTO projects 
                (id, project_name, organisation, geographical_level, 
                link_to_organisation, sk_inspiration)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()),
                    project['project_name'],
                    project['organization'],
                    project['geographic_level'],
                    project['link_to_organization'],
                    inspiration_id
                ))
        
        conn.commit()
        
    except Exception as e:
        ui.notify(f"Error saving: {str(e)}", type='negative')
        logger.error(f"Save failed: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def show_projects_dialog(projects: List[Dict], muse_name: str, muse_color: str) -> bool:
    """Display projects in a dialog with muse-themed styling"""
    with ui.dialog().classes("w-full max-w-2xl") as dialog, ui.card().classes("w-full p-0 overflow-hidden"):
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
        
        with ui.column().classes("w-full p-6 gap-4 relative"):
            # Header with muse reference
            
            ui.label(f"Guided by inspiration, {muse_name} connects you to these projects").classes(
                "text-2xl font-bold text-center text-black"  # Changed from text-white to text-black
            ).style("text-shadow: 0 1px 2px rgba(0,0,0,0.2)")  # Lightened shadow for dark text
            
            # Projects list
            for project in projects:
                with ui.card().classes("w-full p-4 bg-white bg-opacity-90 border-l-4").style(
                    f"border-left-color: {muse_color}"
                ):
                    with ui.column().classes("gap-2"):
                        ui.label(project['project_name']).classes("text-lg font-semibold text-black")
                        ui.label(f"by {project['organization']}").classes("text-md text-gray-800")
                        ui.label(f"Scope: {project['geographic_level']}").classes("text-sm text-gray-600")
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("link", color="primary")
                            ui.link("Visit", project['link_to_organization'], new_tab=True).classes("text-primary")
            
            # Single close button with muse color
            ui.button(
                "Close", 
                on_click=lambda: dialog.submit(True)  # Changed to submit True
            ).classes("w-full mt-4 text-white").style(
                f"background-color: {muse_color} !important;"
                "font-weight: 600;"
                "padding: 12px;"
            )
    
    return dialog

async def handle_share(fact_info: Dict[str, Any], user_input: str, share_button: ui.button):
    """Handle the share button click with cosmic starry loader"""
    if not user_input.strip():
        ui.notify("Please write something first", type='warning')
        return
    
    muse_color = MUSE_COLORS[fact_info['muse']]
    
    # Create cosmic loader with black background
    with ui.column().classes("fixed-full items-center justify-center bg-black z-50") as loader:
        ui.label("Looking through the telescope...").classes("text-3xl font-bold text-white mb-4")
        
        # Add HTML/CSS for animated cosmic background
        ui.add_head_html(f'''
            <style>
                @keyframes twinkle {{
                    0% {{ opacity: 0.2; transform: scale(0.5); }}
                    50% {{ opacity: 1; transform: scale(1); }}
                    100% {{ opacity: 0.2; transform: scale(0.5); }}
                }}
                @keyframes shooting-star {{
                    0% {{ transform: translateX(0) translateY(0); opacity: 0; }}
                    10% {{ opacity: 1; }}
                    100% {{ transform: translateX(100vw) translateY(100vh); opacity: 0; }}
                }}
                .star {{
                    position: absolute;
                    background-color: {muse_color};
                    width: 3px;
                    height: 3px;
                    border-radius: 50%;
                    animation: twinkle 3s infinite ease-in-out;
                    box-shadow: 0 0 5px 1px {muse_color};
                }}
                .shooting-star {{
                    position: absolute;
                    width: 100px;
                    height: 2px;
                    background: linear-gradient(90deg, transparent, {muse_color});
                    transform: rotate(-45deg);
                    animation: shooting-star 3s linear infinite;
                    opacity: 0;
                }}
                .cosmic-dust {{
                    position: absolute;
                    background-color: rgba(255,255,255,0.1);
                    border-radius: 50%;
                }}
            </style>
        ''')
        
        # Container for cosmic elements
        with ui.element('div').classes('fixed-full overflow-hidden'):
            # Generate 50 twinkling stars
            for _ in range(50):
                top = f"{random.uniform(0, 100)}%"
                left = f"{random.uniform(0, 100)}%"
                delay = f"{random.uniform(0, 3)}s"
                duration = f"{random.uniform(2, 4)}s"
                size = f"{random.uniform(2, 5)}px"
                
                ui.html(f'''
                    <div class="star" style="
                        top: {top};
                        left: {left};
                        animation-delay: {delay};
                        animation-duration: {duration};
                        width: {size};
                        height: {size};
                    "></div>
                ''')
            
            # Add some subtle cosmic dust particles
            for _ in range(20):
                top = f"{random.uniform(0, 100)}%"
                left = f"{random.uniform(0, 100)}%"
                size = f"{random.uniform(1, 3)}px"
                
                ui.html(f'''
                    <div class="cosmic-dust" style="
                        top: {top};
                        left: {left};
                        width: {size};
                        height: {size};
                    "></div>
                ''')
            
            # Add occasional shooting stars
            for _ in range(3):
                top = f"{random.uniform(0, 50)}%"
                left = f"{random.uniform(-20, 0)}%"
                delay = f"{random.uniform(0, 8)}s"
                duration = f"{random.uniform(2, 4)}s"
                
                ui.html(f'''
                    <div class="shooting-star" style="
                        top: {top};
                        left: {left};
                        animation-delay: {delay};
                        animation-duration: {duration};
                    "></div>
                ''')
    
    try:
        # Get project recommendations
        projects_data = await get_project_response(fact_info, user_input)
        
        if not projects_data or not projects_data.get('projects'):
            ui.notify("No cosmic connections found today", type='info')
            projects_data = {'projects': []}
        
        # Remove share button
        share_button.delete()
        
        # Show projects dialog
        dialog = show_projects_dialog(
            projects_data['projects'],
            fact_info['muse'],
            muse_color
        )
        await dialog
        
        # Save to database
        save_response(fact_info, user_input, projects_data['projects'])
        ui.notify("Shared with the universe!", type='positive')
        
    except Exception as e:
        ui.notify(f"Stellar interference: {str(e)}", type='negative')
        logger.error(f"Share error: {str(e)}")
    finally:
        loader.delete()

@ui.page("/")
def main():
    """Main page with proper session handling"""
    fact_info = get_todays_fact()
    apply_styles(fact_info['muse'])
    
    with ui.column().classes("main-container"):
        # Logo and header
        with open("backgrounds/logo.png", "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
            ui.html(f'''
                <a href="https://cocoex.xyz" target="_blank" 
                    style="display:block; width:60px; height:60px; margin:10px auto;">
                    <img src="data:image/png;base64,{logo_base64}" 
                        style="width:100%; height:100%; object-fit: contain;">
                </a>
            ''')

        # Header
        ui.label("Today's Muse").classes("muse-subtitle")
        ui.label(fact_info['muse'].upper()).classes("muse-title")
        ui.label(f"for {fact_info['social_cause']}").classes("muse-subtitle")
        
        # Fact Display
        ui.label(fact_info['fun_fact']).classes("fun-fact")
        ui.link("Source", fact_info['fact_check_link']).classes("source-link")
        
        # Question text
        ui.label(fact_info['question_asked']).classes("question-text")
        with ui.column().classes("w-full input-container"):
            user_input = ui.textarea(placeholder="Share your inspiration (max 500 characters)...") \
                .classes("clean-input") \
                .props('maxlength=500')
            
            # Centered share button container
            with ui.row().classes("w-full justify-center") as button_container:
                share_button = ui.button(
                    f"SHARE WITH {fact_info['muse'].upper()}",
                    on_click=lambda: handle_share(fact_info, user_input.value, share_button)
                ).classes("muse-button")

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        port=8080,
        title="Muse Observatory",
        favicon="🔭",
        reload=False
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()
    logger.info(f"Looking at the stars orbiting in the cocoex's universe! 🔭")
    ui.run(
        port=8080,
        title="Muse Observatory",
        favicon="🔭",
        reload=False
    )