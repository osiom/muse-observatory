import random

def get_cosmic_css(muse_color: str, support_color: str, astro_color: str) -> tuple[str, str]:
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');
        
        body {{
            background: linear-gradient(135deg, {support_color} 0%, {muse_color} 100%);
            margin: 0;
            font-family: 'Cormorant Garamond', serif;
            color: #d1c4e9;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
            box-sizing: border-box;
        }}

        .cosmic-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background:
                radial-gradient(circle at 30% 50%, {muse_color}33 0%, transparent 30%),
                radial-gradient(circle at 80% 70%, {muse_color}44 0%, transparent 25%),
                linear-gradient(to bottom, {muse_color}, {support_color});
        }}

        .static-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                repeating-linear-gradient(0deg, rgba(0,0,0,0.15) 0px, 
                rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px),
                repeating-linear-gradient(90deg, rgba(0,0,0,0.15) 0px, 
                rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px);
            opacity: 0.2;
            z-index: -1;
            pointer-events: none;
            animation: static 0.2s infinite;
        }}

        @keyframes static {{
            0% {{ background-position: 0 0; }}
            100% {{ background-position: 3px 3px; }}
        }}

        @keyframes twinkle {{
            0% {{ opacity: 0.2; transform: scale(0.5); }}
            50% {{ opacity: 1; transform: scale(1); }}
            100% {{ opacity: 0.2; transform: scale(0.5); }}
        }}

        @keyframes shooting-star-left-to-right {{
            0% {{ transform: translateX(-100px) translateY(-100px) rotate(-45deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateX(calc(100vw + 100px)) translateY(calc(100vh + 100px)) rotate(-45deg); opacity: 0; }}
        }}

        @keyframes shooting-star-right-to-left {{
            0% {{ transform: translateX(calc(100vw + 100px)) translateY(-100px) rotate(45deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateX(-200px) translateY(calc(100vh + 100px)) rotate(45deg); opacity: 0; }}
        }}

        @keyframes shooting-star-top-to-bottom {{
            0% {{ transform: translateY(-100px); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(calc(100vh + 100px)); opacity: 0; }}
        }}

        @keyframes shooting-star-bottom-to-top {{
            0% {{ transform: translateY(calc(100vh + 100px)); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(-100px); opacity: 0; }}
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}

        .star, .shooting-star, .cosmic-dust {{
            position: absolute;
            z-index: 1000;
            pointer-events: none;
        }}

        .star {{
            background-color: {astro_color};
            border-radius: 50%;
            animation: twinkle 3s infinite ease-in-out;
            box-shadow: 0 0 3px 1px {astro_color};
        }}

        .shooting-star {{
            width: 30px;
            height: 2px;
            background: linear-gradient(90deg, {astro_color}, transparent);
            border-radius: 1px;
            opacity: 0;
            box-shadow: 0 0 10px {astro_color};
        }}

        .cosmic-dust {{
            background-color: rgba(255,255,255,0.3);
            border-radius: 50%;
            animation: float 4s ease-in-out infinite;
        }}
    </style>
    """

    stars_html = ""

    # Twinkling stars
    for _ in range(30):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        delay = random.uniform(0, 3)
        duration = random.uniform(2, 4)
        size = random.uniform(2, 5)
        stars_html += f'''
        <div class="star" style="
            top: {top}%;
            left: {left}%;
            animation-delay: {delay}s;
            animation-duration: {duration}s;
            width: {size}px;
            height: {size}px;
        "></div>
        '''

    # Cosmic dust
    for _ in range(20):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        size = random.uniform(1, 3)
        delay = random.uniform(0, 4)
        stars_html += f'''
        <div class="cosmic-dust" style="
            top: {top}%;
            left: {left}%;
            width: {size}px;
            height: {size}px;
            animation-delay: {delay}s;
        "></div>
        '''

    # Shooting stars from random directions
    directions = [
        "shooting-star-left-to-right",
        "shooting-star-right-to-left",
        "shooting-star-top-to-bottom",
        "shooting-star-bottom-to-top"
    ]

    for _ in range(4):
        direction = random.choice(directions)
        top = random.uniform(-20, 100)
        left = random.uniform(-20, 100)
        delay = random.uniform(0, 6)
        duration = random.uniform(2, 4)
        stars_html += f'''
        <div class="shooting-star" style="
            top: {top}%;
            left: {left}%;
            animation-name: {direction};
            animation-delay: {delay}s;
            animation-duration: {duration}s;
        "></div>
        '''

    return css, stars_html
