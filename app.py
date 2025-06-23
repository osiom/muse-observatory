import asyncio
import base64
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from nicegui import ui
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from db.db import close_db_pool, init_db_pool
from models.schemas import AppInfoResponse
from observatory import observatory
from utils.limiter import limiter
from utils.logger import get_logger

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
    lifespan=lifespan,
)

# --- Rate Limiting Setup ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# --- End Rate Limiting Setup ---


# Health check endpoint
@app.get("/api/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "muse-observatory", "version": "1.0.0"}


# Additional API endpoints
@app.get("/api/info", response_model=AppInfoResponse)
@limiter.limit("10/minute")
async def app_info(request: Request):
    """Get application information."""
    return AppInfoResponse(
        name="Muse Observatory",
        description="Looking at the stars in the universe",
        environment=os.getenv("ENVIRONMENT", "production"),
    )


# Main landing page
@ui.page("/")
def main():
    """Main landing page with terminal-style animation."""
    ui.add_head_html(
        """
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
    """
    )
    ui.add_head_html(
        """
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
            z-index: 10;
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
        .centered-container {
            height: 100vh;                    /* Full viewport height */
            display: flex;
            align-items: center;             /* Vertical centering */
            justify-content: center;         /* Horizontal centering */
            flex-direction: column;
            text-align: center;
        }

        .terminal {
            background-color: #000 !important;
            border: 1px solid #333;
            padding: 2rem;
            width: 600px;
            text-align: center;
            z-index: 100;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
            color: white;
            font-family: 'Cormorant Garamond', serif;
        }

        .init-text {
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(1.2rem, 4vw, 1.8rem);
            color: white;
            display: inline-block;
            position: relative;
        }

        @keyframes blink {
            from, to { opacity: 0; }
            50% { opacity: 1; }
        }

        .dots {
            position: relative;
            color: white;
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(1.2rem, 4vw, 1.8rem);
            display: inline-block;
        }

        .dots span {
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        .dots span:nth-child(1) { animation-delay: 0.5s; }
        .dots span:nth-child(2) { animation-delay: 1s; }
        .dots span:nth-child(3) { animation-delay: 1.5s; }

        .dots::after {
            content: '|';
            position: absolute;
            margin-left: 2px;
            animation: blink 0.75s step-end infinite;
            color: white;
        }

        .loading-completed {
            font-family: 'Cormorant Garamond', serif;
            font-size: clamp(1.2rem, 4vw, 1.8rem);
            color: white;
            display: inline-block;
            position: relative;
            opacity: 0;
            animation: fade-in 0.5s ease-in forwards;
            animation-delay: 2s; /* Appears after all dots finish */
        }

        @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .telescope {
            opacity: 1 !important;
            font-size: clamp(2rem, 8vw, 4rem);
            margin-top: 1rem;
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(0); }
        }

        .prompt {
            color: white;
            font-size: clamp(1rem, 3vw, 1.5rem);
            font-family: 'Cormorant Garamond', serif;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            margin-top: 1.5rem;
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
    """
    )

    # Logo and header
    with open("img/logo.png", "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()
        ui.html(
            f"""
        <div class="logo-container">
            <a href="https://cocoex.xyz" target="_blank">
                <img src="data:image/png;base64,{logo_base64}" class="logo-img">
            </a>
        </div>
        """
        )

    # Create screen container that will animate
    screen = ui.element("div").classes("screen-container")
    # Create noise background
    with screen:
        ui.element("div").classes("noise")
    with ui.column().classes("centered-container"):
        with ui.element("div").classes("terminal"):
            status = ui.html("muse-observatory init |").classes("init-text")
        prompt = ui.label("Press Enter.").classes("prompt").style("opacity: 0")
        ui.html('<div class="telescope">🔭</div>')

    async def animate_loading():
        await asyncio.sleep(0.6)
        status.set_content("muse-observatory init. ")
        await asyncio.sleep(0.6)
        status.set_content("muse-observatory init.. |")
        await asyncio.sleep(0.6)
        status.set_content("muse-observatory init...")
        await asyncio.sleep(0.6)
        status.set_content("muse-observatory init... |")
        await asyncio.sleep(0.6)
        status.set_content("loading completed.")
        await asyncio.sleep(0.7)
        prompt.style("opacity: 1")

    ui.timer(0.5, animate_loading, once=True)  # ✅ Properly scheduled

    # Handle TV closing effect
    def tv_close_and_go():
        """Animate transition to observatory page."""
        screen.classes(add="tv-close")
        ui.timer(0.33, lambda: ui.navigate.to("/observatory"), once=True)

    # Set up click handlers
    screen.on("click", tv_close_and_go)
    prompt.on("click", tv_close_and_go)
    ui.keyboard(on_key=lambda e: tv_close_and_go() if e.key.enter else None)


def configure_nicegui():
    """Configure NiceGUI settings."""
    ui.add_head_html(
        """
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🔭</text></svg>">
    """
    )
    ui.run_with(app, title="Muse Observatory", favicon="🔭")


if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    logger.info("🚀 Looking at the stars orbiting in the cosmos! 🔭")
    logger.info(f"📡 Server starting on {host}:{port}")

    if debug:
        logger.info("🐛 Debug mode enabled")

    configure_nicegui()
    # 🧠 ADD THIS to actually start the server:
    ui.run(host=host, port=port, reload=debug, title="Muse Observatory", favicon="🔭")
