from nicegui import ui
import base64
from pathlib import Path

@ui.page('/landing')
def landing_page():
    # 1. Load your image - ENSURE THIS PATH IS CORRECT
    img_path = Path(__file__).parent / 'backgrounds' / 'landing.png'
    with open(img_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode()

    # 2. CSS with proper escaping and Cormorant Garamond font
    ui.add_head_html(f'''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');
        
        body {{
            margin: 0;
            height: 100vh;
            overflow: hidden;
            font-family: 'Cormorant Garamond', serif;
            cursor: pointer;
            background-color: black; /* Ensures black fallback */
        }}
        .fullscreen-image {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-image: url('data:image/png;base64,{img_base64}');
            background-size: cover;
            background-position: center;
            transition: transform 1s;
            transform-style: preserve-3d;
            backface-visibility: hidden; /* Important for 3D transforms */
        }}
        .fullscreen-image.flipped {{
            transform: rotateY(180deg);
            background-color: rgba(0, 0, 0, 0.3); /* Black with 30% opacity */
        }}
        .prompt {{
            position: fixed;
            bottom: 10%;
            left: 0;
            right: 0;
            text-align: center;
            color: white;
            font-size: 2rem;
            font-family: 'Cormorant Garamond', serif;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            pointer-events: none;
            z-index: 10; /* Ensure text stays above everything */
        }}
    </style>
    ''')

    # 3. Create fullscreen image element
    image = ui.element('div').classes('fullscreen-image')
    ui.label("Press Enter or click to begin").classes('prompt')

    # 4. Handle both click and Enter key
    def flip_and_go():
        image.classes(add='flipped')
        ui.timer(0.0000000000001, lambda: ui.navigate.to('/observatory'), once=True)
    
    # Click anywhere on the page
    image.on('click', flip_and_go)
    ui.keyboard(on_key=lambda e: flip_and_go() if e.key.enter else None)