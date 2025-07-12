import random


def get_opposite_color(hex_color: str):
    """Get complementary color by inverting RGB"""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"#{255-r:02x}{255-g:02x}{255-b:02x}"


def get_text_css(color: str):
    css = f"""
    <style>
            .main-container {{
                width: calc(100% - 1rem);
                max-width: none;
                margin: 0 0.5rem;
                padding: 0.5rem;
                padding-top: 0;  /* Remove top padding */
                text-align: center;
                box-sizing: border-box;
            }}
            /* Text styles */
            .muse-title {{
                font-size: 46px;
                font-weight: bold;
                text-align: center;
                margin: 0 0 5px 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            }}

            .muse-subtitle {{
                font-size: 20px;
                text-align: center;
                margin: 0 0 5px 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            }}

            .fun-fact {{
                font-size: 18px;
                font-style: normal;
                text-align: center;
                line-height: 1.6;
                margin: 0 0 5px 0;
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
                min-height: 35px !important;
                margin: 0 auto 10px auto !important;
                font-size: 16px !important;
                background: white !important;
                color: black !important;
                border: 2px solid {color} !important;
                border-radius: 12px !important;
                padding: 10px !important;           /* Adjust padding for shorter height */
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
                padding: 10px 30px !important;
                border: 3px solid {color} !important;
                border-radius: 24px !important;
                cursor: pointer;
                margin-top: 5px !important;
                transition: all 0.3s;
            }}
            .notification-container, .notification {{
                z-index: 999* !important;  /* super high to be on top */
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
                min-height: 66px; /* Prevents layout shift when text appears */
                position: relative;
                overflow: hidden; /* Prevents content from breaking out */
            }}

            /* Question text */
            .question-text {{
                font-size: 16px;
                width: 100%;               /* ensures it respects parent width */
                box-sizing: border-box;   /* includes padding in width */
                margin: 0 0 10px 0;
                padding: 0 1rem;
                font-style: normal;
                text-align: center;
                line-height: 1.4;
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


def get_cosmic_css(
    muse_color: str, support_color: str, astro_color: str
) -> tuple[str, str]:
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');

        body {{
            background:
                /* Primary gradient using muse and astro colors */
                radial-gradient(ellipse at 30% 20%, {muse_color}40 0%, transparent 50%),
                radial-gradient(ellipse at 70% 80%, {astro_color}35 0%, transparent 60%),
                radial-gradient(circle at 20% 60%, {muse_color}25 0%, transparent 40%),
                radial-gradient(circle at 80% 40%, {astro_color}30 0%, transparent 45%),
                /* Deep space base with muse/astro undertones */
                linear-gradient(135deg, {muse_color}08 0%, {astro_color}12 30%, rgba(5,5,25,0.95) 70%, rgba(0,0,0,0.98) 100%),
                /* Final dark overlay */
                radial-gradient(ellipse at center, rgba(10,10,30,0.6) 0%, rgba(0,0,0,0.9) 100%);
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
                /* Enhanced nebula clouds with stronger muse/astro colors */
                radial-gradient(ellipse 700px 400px at 15% 25%, {muse_color}35 0%, {muse_color}15 30%, transparent 60%),
                radial-gradient(ellipse 600px 800px at 85% 75%, {astro_color}40 0%, {astro_color}20 25%, transparent 50%),
                radial-gradient(ellipse 900px 300px at 50% 5%, {astro_color}25 0%, {muse_color}12 40%, transparent 70%),
                radial-gradient(ellipse 400px 500px at 5% 85%, {muse_color}30 0%, {astro_color}18 35%, transparent 55%),
                radial-gradient(ellipse 500px 600px at 90% 15%, {astro_color}28 0%, transparent 45%),
                /* Cosmic energy streams */
                linear-gradient(45deg, transparent 40%, {muse_color}08 50%, transparent 60%),
                linear-gradient(-45deg, transparent 35%, {astro_color}10 50%, transparent 65%),
                /* Distant galaxy glows enhanced with theme colors */
                radial-gradient(circle 200px at 75% 25%, {astro_color}20 0%, rgba(255,255,255,0.05) 50%, transparent 70%),
                radial-gradient(circle 150px at 25% 75%, {muse_color}15 0%, rgba(255,255,255,0.04) 50%, transparent 70%),
                radial-gradient(circle 120px at 60% 60%, {astro_color}12 0%, transparent 70%);
        }}

        .dust-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                /* Cosmic dust with color tints */
                repeating-linear-gradient(45deg,
                    transparent 0px,
                    {muse_color}02 0.5px,
                    rgba(255,255,255,0.008) 1px,
                    transparent 2px,
                    transparent 100px),
                repeating-linear-gradient(-45deg,
                    transparent 0px,
                    {astro_color}02 0.5px,
                    rgba(255,255,255,0.006) 1px,
                    transparent 2px,
                    transparent 150px),
                repeating-linear-gradient(135deg,
                    transparent 0px,
                    {muse_color}01 1px,
                    transparent 2px,
                    transparent 200px);
            opacity: 0.7;
            z-index: -1;
            pointer-events: none;
        }}

        @keyframes twinkle {{
            0% {{ opacity: 0.3; transform: scale(0.8); }}
            25% {{ opacity: 1; transform: scale(1.2); }}
            50% {{ opacity: 0.6; transform: scale(1); }}
            75% {{ opacity: 1; transform: scale(1.1); }}
            100% {{ opacity: 0.3; transform: scale(0.8); }}
        }}

        @keyframes pulsar {{
            0% {{ opacity: 0.5; transform: scale(1); box-shadow: 0 0 5px {muse_color}; }}
            50% {{ opacity: 1; transform: scale(1.5); box-shadow: 0 0 20px {muse_color}, 0 0 30px {astro_color}80; }}
            100% {{ opacity: 0.5; transform: scale(1); box-shadow: 0 0 5px {muse_color}; }}
        }}

        @keyframes nebula-drift {{
            0% {{ transform: translateX(0) rotate(0deg); opacity: 0.3; }}
            50% {{ transform: translateX(15px) rotate(2deg); opacity: 0.5; }}
            100% {{ transform: translateX(0) rotate(0deg); opacity: 0.3; }}
        }}

        @keyframes shooting-star-left-to-right {{
            0% {{ transform: translateX(-100px) translateY(-100px) rotate(-45deg); opacity: 0; }}
            5% {{ opacity: 1; }}
            95% {{ opacity: 1; }}
            100% {{ transform: translateX(calc(100vw + 100px)) translateY(calc(100vh + 100px)) rotate(-45deg); opacity: 0; }}
        }}

        @keyframes shooting-star-right-to-left {{
            0% {{ transform: translateX(calc(100vw + 100px)) translateY(-100px) rotate(45deg); opacity: 0; }}
            5% {{ opacity: 1; }}
            95% {{ opacity: 1; }}
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
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            33% {{ transform: translateY(-8px) rotate(1deg); }}
            66% {{ transform: translateY(-15px) rotate(-1deg); }}
        }}

        .star, .shooting-star, .cosmic-dust, .nebula-particle, .pulsar {{
            position: absolute;
            z-index: 1000;
            pointer-events: none;
        }}

        .star {{
            background-color: {get_opposite_color(astro_color)};
            border-radius: 50%;
            animation: twinkle 4s infinite ease-in-out;
        }}

        .star.distant {{
            background-color: {astro_color}90;
            box-shadow: 0 0 2px {astro_color}60;
        }}

        .star.bright {{
            background-color: #ffffff;
            box-shadow: 0 0 8px #ffffff80, 0 0 15px {astro_color}40;
        }}

        .star.colored {{
            background-color: {muse_color};
            box-shadow: 0 0 4px {muse_color}80;
        }}

        .pulsar {{
            background-color: {muse_color};
            border-radius: 50%;
            animation: pulsar 2s infinite ease-in-out;
        }}

        .shooting-star {{
            background: linear-gradient(90deg, {astro_color}, {muse_color}80, transparent);
            border-radius: 1px;
            opacity: 0;
            box-shadow: 0 0 15px {astro_color}60, 0 0 25px {muse_color}40;
        }}

        .cosmic-dust {{
            background-color: rgba(255,255,255,0.4);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }}

        .nebula-particle {{
            background: radial-gradient(circle, {muse_color}70 0%, {astro_color}40 40%, transparent 70%);
            border-radius: 50%;
            animation: nebula-drift 20s ease-in-out infinite;
            filter: blur(1px);
        }}
    </style>
    """

    stars_html = ""

    # Mixed star types for realistic variety
    star_types = [
        {"class": "star distant", "weight": 0.5},
        {"class": "star bright", "weight": 0.3},
        {"class": "star colored", "weight": 0.1},
        {"class": "pulsar", "weight": 0.02},
    ]

    # Create more varied stars
    for _ in range(50):
        star_type = random.choices(
            star_types, weights=[t["weight"] for t in star_types]
        )[0]
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        delay = random.uniform(0, 4)
        duration = random.uniform(3, 8)

        if "pulsar" in star_type["class"]:
            size = random.uniform(2, 4)
            duration = random.uniform(1.5, 3)
        elif "bright" in star_type["class"]:
            size = random.uniform(2, 6)
        else:
            size = random.uniform(0.5, 3)

        stars_html += f"""
        <div class="{star_type['class']}" style="
            top: {top}%;
            left: {left}%;
            animation-delay: {delay}s;
            animation-duration: {duration}s;
            width: {size}px;
            height: {size}px;
        "></div>
        """

    # Enhanced nebula particles with more muse/astro color influence
    for _ in range(12):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        size = random.uniform(10, 30)
        delay = random.uniform(0, 20)
        stars_html += f"""
        <div class="nebula-particle" style="
            top: {top}%;
            left: {left}%;
            width: {size}px;
            height: {size}px;
            animation-delay: {delay}s;
        "></div>
        """

    # Enhanced cosmic dust
    for _ in range(7):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        size = random.uniform(0.5, 2)
        delay = random.uniform(0, 6)
        stars_html += f"""
        <div class="cosmic-dust" style="
            top: {top}%;
            left: {left}%;
            width: {size}px;
            height: {size}px;
            animation-delay: {delay}s;
        "></div>
        """

    # More realistic shooting stars with theme colors
    directions = [
        "shooting-star-left-to-right",
        "shooting-star-right-to-left"
        # "shooting-star-top-to-bottom",
        # "shooting-star-bottom-to-top"
    ]

    for _ in range(1):
        direction = random.choice(directions)
        top = random.uniform(-20, 100)
        left = random.uniform(-20, 100)
        delay = random.uniform(0, 20)
        duration = random.uniform(1.5, 3.5)
        width = random.uniform(40, 80)
        height = random.uniform(1, 3)

        stars_html += f"""
        <div class="shooting-star" style="
            top: {top}%;
            left: {left}%;
            width: {width}px;
            height: {height}px;
            animation-name: {direction};
            animation-delay: {delay}s;
            animation-duration: {duration}s;
            animation-iteration-count: infinite;
        "></div>
        """

    return css, stars_html


def get_load_cosmic_css(color: str) -> tuple[str, str]:
    css = f"""
    <style>
        @keyframes twinkle {{
            0% {{ opacity: 0.2; transform: scale(0.5); }}
            50% {{ opacity: 1; transform: scale(1); }}
            100% {{ opacity: 0.2; transform: scale(0.5); }}
        }}
        @keyframes shooting-star {{
            0% {{ transform: translateX(-100px) translateY(-100px) rotate(-45deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateX(calc(100vw + 100px)) translateY(calc(100vh + 100px)) rotate(-45deg); opacity: 0; }}
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        .cosmic-loader {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 9999 !important;
            pointer-events: none;
        }}
        .star {{
            position: absolute !important;
            background-color: {color} !important;
            width: 3px !important;
            height: 3px !important;
            border-radius: 50% !important;
            animation: twinkle 3s infinite ease-in-out !important;
            box-shadow: 0 0 8px 2px {color} !important;
            z-index: 10000 !important;
        }}
    </style>
    """
    stars_html = ""
    for _ in range(50):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        delay = random.uniform(0, 3)
        duration = random.uniform(1, 3)
        size = random.uniform(2, 5)

        stars_html += f"""
            <div class="star" style="
                top: {top}%;
                left: {left}%;
                animation-delay: {delay}s;
                animation-duration: {duration}s;
                width: {size}px;
                height: {size}px;
            "></div>
        """

    return css, stars_html
