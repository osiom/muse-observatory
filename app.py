from datetime import datetime
from typing import Dict, Any, List
import uuid
import random
import base64
from psycopg2.extras import RealDictCursor
from nicegui import ui

from config.db import get_db_connection, return_db_connection
from config.styles import MUSE_COLORS, get_cosmic_css
from utils.media import get_base64_comet
from logger import get_logger
from utils.projects import get_project_response

logger = get_logger(__name__)

def apply_styles(muse_name: str):
    """Integrated styles combining styles.py with terminal effects and cosmic enhancements"""
    color = MUSE_COLORS.get(muse_name, "#7F49A1")
    
    # 1. Base cosmic styles from styles.py
    ui.add_head_html(get_cosmic_css(muse_name))
    ui.add_head_html('''
    <style>
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
    </style>
    ''')

    # 3. Terminal text animation (new)
    ui.add_head_html(f'''
    <style>
        /* Question terminal styling */
        .terminal-question {{
            position: relative;
            display: inline-block;
            min-width: 20px;
        }}
        .terminal-question::after {{
            content: '|';
            position: absolute;
            right: -10px;
            color: {color};
            animation: blink 1s step-end infinite;
            visibility: hidden; /* Initially hidden */
        }}
        .terminal-question.completed::after {{
            visibility: visible; /* Show when typing done */
        }}
        @keyframes blink {{
            from, to {{ opacity: 0; }}
            50% {{ opacity: 1; }}
        }}
    </style>

    <script>
        function typeQuestion(element) {{
            const text = element.textContent;
            element.textContent = '';
            element.classList.remove('completed');
            
            let i = 0;
            const speed = 70; // Medium typing speed
            
            function type() {{
                if (i < text.length) {{
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }} else {{
                    element.classList.add('completed'); // Triggers cursor visibility
                }}
            }}
            type();
        }}
        
        document.addEventListener('DOMContentLoaded', () => {{
            // Start typing after slight delay for visual polish
            setTimeout(() => {{
                document.querySelectorAll('.terminal-question').forEach(typeQuestion);
            }}, 500);
        }});
    </script>
    ''')

    ui.add_head_html(f'''
    <style>
        .main-container {{
            width: 100%;
            max-width: 900px;  /* Adjust as needed */
            margin: 0 auto;
            padding: 2rem;
            text-align: center; /* Center text content */
        }}

        /* Text styles */
        .muse-title {{
            font-size: 52px;
            font-weight: bold;
            text-align: center;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}

        .muse-subtitle {{
            font-size: 24px;
            text-align: center;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}

        .fun-fact {{
            font-size: 22px;
            font-style: normal;
            text-align: center;
            line-height: 1.6;
            margin: 0;
            max-width: 800px;
            text-shadow: 0 2px 2px rgba(0,0,0,0.3);
        }}

        /* Input section */
        .input-section {{
            width: 100%;
            max-width: 800px;
            margin: 2rem 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        /* Form elements */
        .clean-input {{
            width: 65% !important;
            min-height: 100px !important;
            margin: 0 auto !important;
            font-size: 16px !important;
            background: white !important;
            color: black !important;
            border: 2px solid {color} !important;
            border-radius: 12px !important;
            padding: 16px !important;
            font-family: 'Cormorant Garamond' !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .clean-input::placeholder {{
            color: #666 !important;
            font-style: italic;
            opacity: 1 !important;
        }}

        /* Buttons */
        .muse-button {{
            background-color: {color} !important;
            color: white !important;
            font-size: 16px !important;
            padding: 12px 36px !important;
            border: none !important;
            border-radius: 8px !important;
            cursor: pointer;
            transition: all 0.3s;
            margin: 0 auto;
        }}

        .muse-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }}

        /* Dialog styles */
        .dialog-button {{
            background-color: transparent !important;
            color: {color} !important;
            font-size: 16px !important;
            padding: 8px 24px !important;
            border: 3px solid {color} !important;
            border-radius: 24px !important;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .dialog-button:hover {{
            background-color: {color} !important;
            color: white !important;
        }}

        .muse-title,
        .muse-subtitle,
        .fun-fact,
        .question-text,
        .source-link {{
            text-align: center !important;
            margin-left: auto;
            margin-right: auto;
        }}

        /* Question text */
        .question-text {{
            font-size: 21px;
            font-style: italic;
            text-align: center;
            margin: 20px auto;
            max-width: 800px;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            line-height: 1.4;
            padding: 0 20px;
        }}

        /* Input container */
        .input-container {{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0 auto;
        }}

        /* Prompt text */
        .write-prompt {{
            text-align: center;
            color: white;
            font-style: italic;
            margin: 12px;
            font-size: 18px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        }}

        /* Button container */
        .button-container {{
            display: flex;
            justify-content: center;
            width: 100%;
            margin: 10px;
        }}
    </style>
    ''')

def get_todays_fact() -> Dict[str, Any]:
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
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
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)  # Return to pool instead of closing


def save_response(fact_info: Dict[str, Any], user_input: str, projects: List[Dict]):
    """Save both inspiration and projects with connection pooling"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        inspiration_id = str(uuid.uuid4())
        # Save inspiration
        cursor.execute("""
            INSERT INTO inspirations 
            (date, id, day_of_week, social_cause, muse, user_inspiration)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                datetime.now().date(),
                inspiration_id,
                datetime.now().strftime('%A'),
                fact_info['social_cause'],
                fact_info['muse'],
                user_input
            ))
        
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
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)  # Return to pool instead of closing

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
                on_click=lambda: dialog.submit(True)
            ).classes("dialog-button w-full mt-4")
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
                    width: 6px;
                    height: 6px;
                    background: url("data:image/png;base64,{get_base64_comet(fact_info['muse'], muse_color)}");
                    background-size: contain;
                    background-repeat: no-repeat;
                    background-position: center;
                    transform: rotate(-45deg);
                    animation: shooting-star 3s linear infinite;
                    opacity: 0;
                    filter: drop-shadow(0 0 5px {muse_color});
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
            for _ in range(5):
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
        ui.notify(f"Shared with the {fact_info['muse']}!", type='positive')
    except Exception as e:
        ui.notify(f"Stellar interference: {str(e)}", type='negative')
        logger.error(f"Share error: {str(e)}")
    finally:
        loader.delete()

@ui.page("/observatory")
def observatory():
    fact_info = get_todays_fact()
    apply_styles(fact_info['muse'])
    
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
            ui.label("Today's Muse").classes("muse-subtitle")
            ui.label(fact_info['muse'].upper()).classes("muse-title text-center")
            ui.label(f"for {fact_info['social_cause']}").classes("muse-subtitle text-center")
            
            # Terminal-style elements
            ui.label(fact_info['fun_fact']).classes("fun-fact text-center")
            ui.link("Source", fact_info['fact_check_link']).classes("source-link text-center")
            
            # Question and input
            ui.label(fact_info['question_asked']).classes("question-text terminal-question text-center")
            
            with ui.column().classes("input-container w-full mx-auto"):
                user_input = ui.textarea(placeholder="Share your inspiration...") \
                    .classes("clean-input mx-auto")
                
                ui.button(
                    f"SHARE WITH {fact_info['muse'].upper()}",
                    on_click=lambda: handle_share(fact_info, user_input.value)
                ).classes("muse-button mx-auto")
