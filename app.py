import os
import base64
import streamlit as st
import psycopg2
import uuid
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "muse_observatory"),
    "user": os.getenv("DB_USER", "museuser"),
    "password": os.getenv("DB_PASSWORD", "musepassword"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_db_connection():
    """Create a database connection"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def get_todays_fact():
    """Get today's fun fact from the database"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT * FROM daily_facts WHERE date = %s", (today,))
    fact = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if fact:
        return dict(fact)
    else:
        # If no fact for today is found, get the most recent one
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM daily_facts ORDER BY date DESC LIMIT 1")
        fact = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if fact:
            return dict(fact)
        else:
            # Fallback if no facts at all
            return {
                "celestial_body": "No Muse Available",
                "fun_fact": "There are no fun facts available yet. Please check back later.",
                "social_cause": "Unknown",
                "question_asked": "Unknown"
            }

def get_base64_of_gif(gif_file):
    """Convert GIF to base64 for embedding in CSS"""
    with open(gif_file, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

def get_base64_of_image(image_file):
    """Convert image to base64 for embedding in HTML"""
    with open(image_file, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()    

def set_gif_background(gif_path):
    """Set the GIF as background using CSS"""
    base64_gif = get_base64_of_gif(gif_path)
    
    # CSS to set the GIF as background
    background_css = f"""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');
    
    .stApp {{
        background-image: url("data:image/gif;base64,{base64_gif}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .top-image {{
        display: block;
        margin: 0 auto 20px auto;
        max-width: 150px;  # Adjust as needed
    }}
    /* Text styling with font family */
    .muse-title {{
        font-size: 56px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0px;
        margin-top: 0px;
        color: white;
        font-family: 'Cormorant Garamond', Georgia, serif;
    }}
    
    .muse-subtitle {{
        font-size: 32px;
        text-align: center;
        margin-bottom: 0px;
        color: white;
        font-family: 'Cormorant Garamond', Georgia, serif;
    }}
    
    .muse-fact-check {{
        font-size: 18px;
        text-align: center;
        margin-bottom: 0px;
        color: white;
        font-family: 'Cormorant Garamond', Georgia, serif;
    }}
    

    .fun-fact {{
        font-size: 24px;
        font-style: italic;
        text-align: center;
        line-height: 1.5;
        color: white;
        font-family: 'Cormorant Garamond', Georgia, serif;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """
    
    return background_css

def main():
    st.set_page_config(
        page_title="The Muse Observatory",
        page_icon="🔭",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Get today's fact
    fact_info = get_todays_fact()
    
    # Select the appropriate GIF background based on the day
    day_of_week = datetime.now().weekday()
    
    # Path to your GIF files - adjust these to your actual file paths
    gif_paths = {
        0: "backgrounds/lunes.gif",  # Monday
        1: "backgrounds/ares.gif",  # Tuesday
        2: "backgrounds/rabu.gif",  # Wednesday
        3: "backgrounds/thunor.gif",  # Thursday
        4: "backgrounds/shukra.gif",  # Friday
        5: "backgrounds/dosei.gif",  # Saturday
        6: "backgrounds/solis.gif",  # Sunday
    }
    
    # Get today's GIF path, use Monday as fallback
    gif_path = gif_paths.get(day_of_week, gif_paths[0])
    
    # Apply the GIF background
    st.markdown(set_gif_background(gif_path), unsafe_allow_html=True)
    
    # Content container with semi-transparent background
    st.markdown("<div class='content-container'>", unsafe_allow_html=True)
    
    # Display the muse name and social cause
    image_path = 'backgrounds/cocoex-logo.png'  # Update this to your actual image path
    base64_image = get_base64_of_image(image_path)
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src="data:image/png;base64,{base64_image}" style="max-width: 75px;">
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown(f"<div class='muse-subtitle'>Today's Muse</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='muse-title'>{fact_info['muse']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='muse-subtitle'>for {fact_info['social_cause']}</div>", unsafe_allow_html=True)
    
    # Display a divider
    st.markdown("<hr style='border-color: white;'>", unsafe_allow_html=True)
    
    # Display the fun fact
    st.markdown(f"<div class='fun-fact'>{fact_info['fun_fact']} - <a href='{fact_info['fact_check_link']}' target='_blank'>Source :)</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
        
    # Add a divider before the input area
    st.markdown("<hr style='border-color: white; margin-top: 30px;'>", unsafe_allow_html=True)

# Add custom CSS for the input area
    st.markdown("""
        <style>
        /* Import Google Font (repeated to ensure it's available) */
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');

        .user-input-section {
            font-size: 20px;
            font-style: italic;
            text-align: center;
            margin-bottom: 0px;
            color: white;
            font-family: 'Cormorant Garamond', Georgia, serif;
        }
        .input-label {
            color: white;
            font-size: 22px;
            margin-bottom: 12px;
            font-family: 'Cormorant Garamond', Georgia, serif;
            letter-spacing: 1px;
            font-weight: 600;
        }

        .stTextArea textarea {
            background-color: white !important;
            color: #333 !important;
            border: 0px solid #ccc !important;
            border-radius: 0px !important;
            padding: 5px !important;
            font-family: 'Cormorant Garamond', Georgia, serif !important;
        }

        .stTextArea textarea:focus {
            outline: none !important;
            box-shadow: none !important;
            border-color: #ccc !important;
        }

        .stTextArea textarea::placeholder {
            color: #444 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Create a heading for the input section
    st.markdown(f"<div class='user-input-section'> What's your take? <p class='input-label'></p></div>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        textarea::placeholder {
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)
    # Create a text area for paragraph input
    user_paragraph = st.text_area(
        "",  # Empty label since we're using custom styled label above
        height=100,
        max_chars=100,
        placeholder=f"{fact_info['question_asked']}"
    )

    # Add a send button with centered styling
    st.markdown("""
        <style>
        div.stButton > button {
            margin: 0 auto;
            display: block;
            font-family: 'Cormorant Garamond', Georgia, serif !important;
            font-size: 22px !important;
            font-weight: 600;
            color: white !important;
            background-color: #333 !important;
            border-radius: 12px;
            padding: 8px 24px;
            border: 1px solid #aaa;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #444 !important;
            border-color: #999;
            cursor: pointer;
        }                
        </style>
        """, unsafe_allow_html=True)
    # Add a send button
    send_button = st.button(f"Share with {fact_info['muse']}")

    # Handle the button click
    if send_button:
        if user_paragraph:
            try:
                # Get current date info
                current_date = datetime.now().date()
                day_name = current_date.strftime('%A')
                response_uuid = uuid.uuid4()
                # Connect to database
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Insert the user's input into the inspirations table
                cursor.execute("""
                    INSERT INTO inspirations 
                    (date, id, day_of_week, social_cause, muse, user_inspiration)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    current_date,
                    response_uuid,
                    day_name,
                    fact_info['social_cause'],
                    fact_info['muse'],  # Using celestial_body as animal_subject
                    user_paragraph,
                ))
                
                # Commit the transaction and close connection
                conn.commit()
                cursor.close()
                conn.close()
                
                st.success("Your inspiration has been saved successfully!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please enter a message before sending.")

if __name__ == "__main__":
    main()
