import asyncio
import base64
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from nicegui import app as nicegui_app
from nicegui import ui
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from tinydb import Query

from db.db import check_db_access, search_with_logging
from models.schemas import AppInfoResponse
from observatory import observatory
from utils.limiter import limiter
from utils.logger import get_logger

logger = get_logger(__name__)


class LocalOnlyMiddleware(BaseHTTPMiddleware):
    """Middleware to restrict API access to local requests only."""

    def __init__(
        self: "LocalOnlyMiddleware",
        app: FastAPI,
        local_prefixes: Optional[List[str]] = None,
    ) -> None:
        super().__init__(app)
        self.local_prefixes = local_prefixes or ["/api/"]
        logger.info(
            f"🔒 Restricting access to {self.local_prefixes} for local requests only"
        )

    async def dispatch(
        self: "LocalOnlyMiddleware", request: Request, call_next: Callable
    ) -> JSONResponse:
        # Get client IP
        client_host = request.client.host if request.client else None
        path = request.url.path

        # Check if path starts with any of the protected prefixes
        is_protected_path = any(
            path.startswith(prefix) for prefix in self.local_prefixes
        )

        # Allow access only if not protected or client is local
        if is_protected_path and not self._is_local_request(client_host):
            logger.warning(f"🚫 Blocked non-local access to {path} from {client_host}")
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Access denied: API endpoints can only be accessed from localhost"
                },
            )

        # Continue processing the request
        return await call_next(request)

    def _is_local_request(
        self: "LocalOnlyMiddleware", client_host: Optional[str]
    ) -> bool:
        """Check if the request is coming from the local machine."""
        local_ips = {"localhost", "127.0.0.1", "::1", "0.0.0.0", None}
        return client_host in local_ips


# Application lifespan manager - simplified
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger.info("🔭 Starting Muse Observatory...")
    try:
        # Check database access using our centralized function
        if check_db_access():
            logger.info("✅ Database initialized and accessible")
        else:
            logger.error(
                "❌ Database is not accessible. Application may not function correctly."
            )
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        logger.warning("Application starting despite database initialization failure")

    yield

    # No explicit shutdown actions needed for TinyDB
    logger.info("🔄 Shutting down Muse Observatory...")


# --- Rate Limiting Setup ---
nicegui_app.state.limiter = limiter
nicegui_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# --- End Rate Limiting Setup ---

# --- Apply Local Only Middleware ---
nicegui_app.add_middleware(LocalOnlyMiddleware)
# --- End Apply Local Only Middleware ---


# Health check endpoint
@nicegui_app.get("/api/health")
@limiter.limit("5/minute")
async def health_check(request: Request):
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "muse-observatory", "version": "1.0.0"}


# Additional API endpoints
@nicegui_app.get("/api/info", response_model=AppInfoResponse)
@limiter.limit("5/minute")
async def app_info(request: Request):
    """Get application information."""
    return AppInfoResponse(
        name="Muse Observatory",
        description="Looking at the stars in the universe",
        environment=os.getenv("ENVIRONMENT", "production"),
    )


@nicegui_app.get("/api/tokens")
@limiter.limit("10/minute")
async def token_usage_stats(request: Request):
    """Get token usage statistics per day."""
    logger.info("🔍 Retrieving token usage statistics")

    # Default to the last 7 days if not specified
    days = 7

    try:
        # Calculate date range
        today = datetime.now().strftime("%Y-%m-%d")
        dates = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            dates.append(date)

        Usage = Query()
        usage_stats = {}

        # Get usage for each date
        for date in dates:
            logs = search_with_logging("openai_usage_log", Usage.date == date)

            # Sum successful API calls
            total_tokens = sum(
                log.get("tokens_used", 0)
                for log in logs
                if log.get("status") == "success"
            )

            # Get breakdown by endpoint
            endpoint_usage = {}
            for log in logs:
                if log.get("status") == "success":
                    endpoint = log.get("endpoint", "unknown")
                    tokens = log.get("tokens_used", 0)
                    endpoint_usage[endpoint] = endpoint_usage.get(endpoint, 0) + tokens

            # Add to results
            usage_stats[date] = {
                "total_tokens": total_tokens,
                "endpoints": endpoint_usage,
            }

        logger.info(f"✅ Retrieved token usage for {len(dates)} days")
        return JSONResponse(
            content={
                "usage_per_day": usage_stats,
                "total_tokens": sum(
                    day_stats["total_tokens"] for day_stats in usage_stats.values()
                ),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error retrieving token usage: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to retrieve token usage: {str(e)}"},
        )


@nicegui_app.get("/api/stats")
async def get_rate_limit_stats():
    logger.info("📊 Starting to gather rate limit stats from temporary storage...")
    storage = nicegui_app.state.limiter._storage
    stats = {}

    for key, value in storage.storage.items():
        logger.debug(f"🔑 Key: {key} | 🔢 Value: {value}")
        try:
            count = int(value)
        except Exception:
            logger.warning(
                f"⚠️ Failed to convert value to int for key: {key} | value: {value}"
            )
            continue

        if key.startswith("LIMITER/"):
            parts = key.split("/")
            if len(parts) >= 3:
                ip = parts[1]
                stats[ip] = stats.get(ip, 0) + count
                logger.debug(f"🖥️ Count updated for IP {ip}: {stats[ip]}")

    logger.info(
        f"✅ Completed gathering stats: {len(stats)} IPs found with rate limiting data"
    )
    return JSONResponse(content=stats)


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
            status = ui.html("muse-observatory initialisation |").classes("init-text")
        prompt = ui.label("Press Enter.").classes("prompt").style("opacity: 0")
        ui.html('<div class="telescope">🔭</div>')

    async def animate_loading():
        await asyncio.sleep(0.6)
        status.set_content("muse-observatory initialisation ")
        await asyncio.sleep(0.6)
        status.set_content("muse-observatory initialisation.. |")
        await asyncio.sleep(0.6)
        status.set_content("muse-observatory initialisation...")
        await asyncio.sleep(0.6)
        status.set_content("muse-observatory initialisation... |")
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
    ui.run_with(nicegui_app, title="Muse Observatory", favicon="🔭")


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
    # 🧠 Actually start the server:
    ui.run(host=host, port=port, reload=debug, title="Muse Observatory", favicon="🔭")
