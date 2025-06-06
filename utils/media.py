import base64
import logging
from logger import get_logger

logger = get_logger(__name__)

def get_base64_comet(comet_path: str, muse_color: str) -> str:
    """Get base64-encoded comet image with colored dot fallback"""
    try:
        with open(comet_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        logger.warning(f"Comet image not found at {comet_path}: {e}")
        # Create SVG fallback
        svg_dot = f'''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="12" fill="{muse_color}"/>
        </svg>
        '''.encode('utf-8')
        return base64.b64encode(svg_dot).decode()