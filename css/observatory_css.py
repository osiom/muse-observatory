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
                color: #FFFFFF;
            }}

            .muse-subtitle {{
                font-size: 20px;
                text-align: center;
                margin: 0 0 5px 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5);
                color: #FFFFFF;
            }}

            .fun-fact {{
                font-size: 18px;
                font-style: normal;
                text-align: center;
                line-height: 1.6;
                margin: 0 0 5px 0;
                max-width: 800px;
                text-shadow: 0 2px 2px rgba(0,0,0,0.3);
                color: #FFFFFF;
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
                text-align: left !important;
            }}

            .clean-input::placeholder {{
                color: #666 !important;
                font-style: italic;
                opacity: 1 !important;
                text-align: left !important;
                padding-left: 4px !important;
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
                color: #FFFFFF;
            }}
            /* Question container styles */
            .question-container {{
                width: 100%;
                max-width: 800px;
                margin: 0 auto;  /* Center the container */
                padding: 1rem;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                align-items: center;  /* Center child elements */
                justify-content: center;
                min-height: 66px;
                position: relative;
                overflow: hidden;
                text-align: center;  /* Force center alignment for all text inside */
            }}

            /* Question text */
            .question-text {{
                font-size: 16px;  /* Reduce from 18px to 16px */
                width: 100%;
                box-sizing: border-box;
                margin: 0 auto 10px auto;  /* Center with auto margins */
                padding: 0 1rem;
                font-style: normal;
                text-align: center !important;  /* Force center alignment */
                line-height: 1.4;  /* Reduce from 1.6 to 1.4 */
                max-width: 800px;
                text-shadow: 0 2px 2px rgba(0,0,0,0.3);
                display: block;  /* Ensure it's a block element */
                color: #FFFFFF;
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

            /* Source link */
            .source-link {{
                color: {color} !important;
                text-decoration: underline !important;
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
            /* Background that emphasizes the muse color more */
            background: linear-gradient(135deg,
                {muse_color}45 0%,
                rgba(0,0,0,0.85) 60%,
                rgba(0,0,0,0.97) 100%);
            margin: 0;
            font-family: 'Cormorant Garamond', serif;
            color: #FFFFFF;
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
                /* Enhanced muse color gradients */
                radial-gradient(ellipse at 10% 30%, {muse_color}50 0%, transparent 70%),
                radial-gradient(ellipse at 20% 20%, {muse_color}35 0%, transparent 60%),
                radial-gradient(ellipse at 80% 70%, {astro_color}30 0%, transparent 70%),
                linear-gradient(to bottom, {muse_color}20, transparent);
        }}

        @keyframes twinkle {{
            0% {{ opacity: 0.3; transform: scale(0.8); }}
            50% {{ opacity: 1; transform: scale(1.1); }}
            100% {{ opacity: 0.3; transform: scale(0.8); }}
        }}

        @keyframes pulsar {{
            0% {{ opacity: 0.5; transform: scale(1); box-shadow: 0 0 5px {muse_color}; }}
            50% {{ opacity: 1; transform: scale(1.5); box-shadow: 0 0 20px {muse_color}, 0 0 30px {astro_color}80; }}
            100% {{ opacity: 0.5; transform: scale(1); box-shadow: 0 0 5px {muse_color}; }}
        }}

        .star, .pulsar {{
            position: absolute;
            z-index: -1;  /* Ensure stars stay behind content */
            pointer-events: none;
        }}

        .star {{
            background-color: {get_opposite_color(astro_color)};
            border-radius: 50%;
            animation: twinkle 4s infinite ease-in-out;
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

        /* Muse color accent at the bottom */
        .bottom-accent {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, {muse_color}, {muse_color}60, {astro_color}30);
            z-index: 1;
        }}
    </style>
    """

    stars_html = '<div class="bottom-accent"></div>'

    # Star types with more emphasis on colored stars (muse color)
    star_types = [
        {"class": "star", "weight": 0.5},
        {"class": "star bright", "weight": 0.3},
        {"class": "star colored", "weight": 0.2},  # Increased weight for colored stars
    ]

    # Increased number of stars
    for _ in range(50):  # Increased from 25 to 40
        star_type = random.choices(
            star_types, weights=[t["weight"] for t in star_types]
        )[0]
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        delay = random.uniform(0, 4)
        duration = random.uniform(3, 8)

        if "bright" in star_type["class"]:
            size = random.uniform(2, 4)
        else:
            size = random.uniform(1, 3)

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

    # Add two pulsars with muse color
    for _ in range(5):  # Increased from 1 to 2
        top = random.uniform(20, 80)
        left = random.uniform(20, 80)
        delay = random.uniform(0, 2)
        size = random.uniform(3, 4)
        stars_html += f"""
        <div class="pulsar" style="
            top: {top}%;
            left: {left}%;
            animation-delay: {delay}s;
            width: {size}px;
            height: {size}px;
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

        .cosmic-loader {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 9999 !important;
            background-color: rgba(12,12,35,0.9) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
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

        /* This is not needed anymore as we're using a card in the UI code */
        .loader-text {{
            display: none;
        }}
    </style>
    """

    # Only create stars, the loading text is now handled by the UI card
    stars_html = ""

    # Add stars for the loading screen
    for _ in range(20):
        top = random.uniform(0, 100)
        left = random.uniform(0, 100)
        delay = random.uniform(0, 3)
        duration = random.uniform(1, 3)
        size = random.uniform(2, 4)

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
