from nicegui import ui
from pathlib import Path

from app import observatory
from config.db import close_db_pool
from logger import get_logger

logger = get_logger(__name__)

@ui.page('/')
def main():
    ui.add_head_html('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            background: #000;
            height: 100vh;
            overflow: hidden;
            font-family: 'Cormorant Garamond', serif;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .screen-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 0.4s ease-in-out;
            clip-path: inset(0% 0% 0% 0%);
        }
        
        .screen-container.tv-close {
            clip-path: inset(0% 50% 0% 50%);
            opacity: 0;
        }
        
        .noise {
            background: url('https://media.giphy.com/media/oEI9uBYSzLpBK/giphy.gif') center center / cover;
            filter: brightness(0.7) contrast(1.3);
            opacity: 0.3;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1;
        }
        
        .terminal {
            background-color: #000 !important; /* Changed to solid black */
            border: 1px solid #222;
            padding: 2rem;
            width: 400px;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .init-text {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.8rem;
            color: white;
            display: inline-block;
            position: relative;
        }
        
        .init-text::after {
            content: '|';
            color: white;
            position: absolute;
            right: -10px;
            animation: blink 0.75s step-end infinite;
        }
        
        @keyframes blink {
            from, to { opacity: 0; }
            50% { opacity: 1; }
        }
        
        .dots {
            display: inline-block;
            width: 30px;
            text-align: left;
        }
        
        .dots span {
            opacity: 0;
            animation: dot-appear 0.5s forwards;
        }
        
        .dots span:nth-child(1) { animation-delay: 0.5s; }
        .dots span:nth-child(2) { animation-delay: 1s; }
        .dots span:nth-child(3) { animation-delay: 1.5s; }
        
        @keyframes dot-appear {
            to { opacity: 1; }
        }
        
        .telescope {
            font-size: 4rem;
            margin-top: 2rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .prompt {
            color: white;
            font-size: 1.5rem;
            font-family: 'Cormorant Garamond', serif;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            margin-top: 1rem;
            opacity: 0;
            animation: fade-in 0.5s forwards;
            animation-delay: 2s;
            cursor: pointer;
        }
        
        @keyframes fade-in {
            to { opacity: 1; }
        }
    </style>
    ''')

    # Create screen container that will animate
    screen = ui.element('div').classes('screen-container')
    
    # Create noise background
    with screen:
        ui.element('div').classes('noise')
    
    # Terminal with solid black background
    with ui.element('div').classes('terminal'):
        with ui.element('div').classes('init-text'):
            ui.html('init observatory')
            with ui.element('span').classes('dots'):
                ui.html('<span>.</span><span>.</span><span>.</span>')
        
        # Prompt line
        prompt = ui.label("press enter...").classes('prompt')
    
    # Telescope emoji
    ui.html('<div class="telescope">🔭</div>')

    # Handle TV closing effect
    def tv_close_and_go():
        screen.classes(add='tv-close')
        ui.timer(0.33, lambda: ui.navigate.to('/observatory'), once=True)
    
    # Set up click handlers
    screen.on('click', tv_close_and_go)
    prompt.on('click', tv_close_and_go)
    ui.keyboard(on_key=lambda e: tv_close_and_go() if e.key.enter else None)

if __name__ in {"__main__", "__mp_main__"}:
    main()
    logger.info(f"Looking at the stars orbiting in the cocoex's universe! 🔭")
    try:
        ui.run(
            port=8080,
            title="Muse Observatory",
            favicon="🔭",
            reload=False
        )
    except Exception as e:
        logger.error(f"Error starting UI: {e}")
    finally:
        close_db_pool()