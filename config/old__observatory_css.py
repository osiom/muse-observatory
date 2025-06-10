import random

def get_logo_css():
    css = f"""
    <style>
        .logo-container {{
            position: fixed;
            top: 20px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: center;
            z-index: 1000;
        }}
        
        .logo-img {{
            width: 60px;
            height: 60px;
            object-fit: contain;
        }}
    </style>
    """
    return css

def get_text_css(color):
    css = f"""
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
                font-size: 46px;
                font-weight: bold;
                text-align: center;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            }}

            .muse-subtitle {{
                font-size: 20px;
                text-align: center;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            }}

            .fun-fact {{
                font-size: 18px;
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
                width: 800px !important;
                max-width: 100% !important;
                min-height: 50px !important;
                margin: 0 auto !important;
                font-size: 16px !important;
                background: white !important;
                color: black !important;
                border: 2px solid {color} !important;
                border-radius: 12px !important;
                padding: 12px !important;           /* Adjust padding for shorter height */
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
                background-color: transparent !important;
                color: white !important;
                font-size: 10px !important;
                font-color: white;
                padding: 12px 36px !important;
                border: 3px solid {color} !important;
                border-radius: 24px !important;
                cursor: pointer;
                transition: all 0.3s;
            }}

            .muse-button:hover {{
                background-color: {color} !important;
                color: white !important;
            }}

            /* Dialog styles */
            .dialog-button {{
                background-color: transparent !important;
                color: {color} !important;
                font-size: 14px !important;
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
            /* Question container styles */
            .question-container {{
                width: 100%;
                max-width: 800px;
                margin: 0 auto;
                padding: 1rem;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 120px; /* Prevents layout shift when text appears */
                position: relative;
                overflow: hidden; /* Prevents content from breaking out */
            }}

            /* Question text */
            .question-text {{
                font-size: 18px;
                width: 100%;               /* ensures it respects parent width */
                box-sizing: border-box;   /* includes padding in width */
                margin: 0 auto;           /* centers it */
                padding: 0 1rem;                       
                font-style: normal;
                text-align: center;
                line-height: 1.6;
                max-width: 800px;
                text-shadow: 0 2px 2px rgba(0,0,0,0.3);
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
                margin: 6px;
                font-size: 18px;
                text-shadow: 0 1px 3px rgba(0,0,0,0.5);
            }}

            /* Button container */
            .button-container {{
                display: flex;
                justify-content: center;
                width: 100%;
                margin: 6px;
            }}
        </style>
        """
    return css

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
    for _ in range(71):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        delay = random.uniform(0, 3)
        duration = random.uniform(2, 10)
        size = random.uniform(1, 5)
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
    for _ in range(50):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        size = random.uniform(1, 2)
        delay = random.uniform(0, 5)
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

    for _ in range(10):
        direction = random.choice(directions)
        top = random.uniform(-20, 100)
        left = random.uniform(-20, 100)
        delay = random.uniform(0, 15)
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
