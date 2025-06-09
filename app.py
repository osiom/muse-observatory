import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from nicegui import ui
from config.db import close_db_pool, init_db_pool
from logger import get_logger
import uvicorn

logger = get_logger(__name__)

# Application lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger.info("🔭 Starting Muse Observatory...")
    try:
        await init_db_pool()
        logger.info("✅ Database connection pool initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise
    
    # Import observatory pages after DB initialization
    try:
        from observatory import observatory
        logger.info("✅ Observatory modules loaded successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import observatory modules: {e}")
        # Don't raise here - let the app start without observatory if needed
    
    yield
    
    # Shutdown
    logger.info("🔄 Shutting down Muse Observatory...")
    try:
        await close_db_pool()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")

# Create FastAPI app with lifespan events
app = FastAPI(
    title="Muse Observatory",
    description="A celestial observation platform",
    version="1.0.0",
    lifespan=lifespan
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "muse-observatory",
        "version": "1.0.0"
    }

# Additional API endpoints
@app.get("/api/info")
async def app_info():
    """Get application information."""
    return {
        "name": "Muse Observatory",
        "description": "Looking at the stars in the universe",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

# Main landing page
@ui.page('/')
def main():
    """Main landing page with terminal-style animation."""
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
            background-color: #000 !important;
            background: #000 !important;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 2rem;
            width: min(400px, 90vw);
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }
        
        .init-text {
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(1.2rem, 4vw, 1.8rem);
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
            font-size: clamp(2rem, 8vw, 4rem);
            margin-top: 2rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .prompt {
            color: white;
            font-size: clamp(1rem, 3vw, 1.5rem);
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
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .terminal {
                padding: 1rem;
                margin-bottom: 1rem;
            }
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
        """Animate transition to observatory page."""
        screen.classes(add='tv-close')
        ui.timer(0.33, lambda: ui.navigate.to('/observatory'), once=True)
    
    # Set up click handlers
    screen.on('click', tv_close_and_go)
    prompt.on('click', tv_close_and_go)
    ui.keyboard(on_key=lambda e: tv_close_and_go() if e.key.enter else None)

# Fallback observatory page (in case the import fails)
@ui.page('/observatory')
def observatory_fallback():
    """Fallback observatory page."""
    ui.label('🔭 Observatory Loading...').classes('text-2xl text-white')
    ui.label('The observatory module is being initialized.').classes('text-white')

def configure_nicegui():
    """Configure NiceGUI settings."""
    # Set page title and favicon
    ui.run_with(
        app,
        title="Muse Observatory",
        favicon="🔭"
    )

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"🚀 Looking at the stars orbiting in the cosmos! 🔭")
    logger.info(f"📡 Server starting on {host}:{port}")
    
    if debug:
        logger.info("🐛 Debug mode enabled")
    
    # Configure and run NiceGUI with FastAPI
    configure_nicegui()