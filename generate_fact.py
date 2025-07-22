import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from tinydb import Query

from db.db import get_db, get_with_logging, insert_with_logging, search_with_logging
from models.schemas import FunFactModel
from utils.logger import get_logger

logger = get_logger(__name__)
# Load environment variables
load_dotenv()

# Connect to OpenAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# TinyDB setup
DB_DIR = Path(os.getenv("DB_DIR", "db_files"))
DB_FILE = DB_DIR / "muse_observatory.json"
DB_DIR.mkdir(exist_ok=True)

MUSES = {
    0: {
        "muse": "Lunes",
        "day_name": "Monday",
        "celestial_body": "Moon",
        "color": "indigo white",
        "note": "Re",
        "cause": "Water",
    },
    1: {
        "muse": "Ares",
        "day_name": "Tuesday",
        "celestial_body": "Mars",
        "color": "red",
        "note": "Si",
        "cause": "Reforestation",
    },
    2: {
        "muse": "Rabu",
        "day_name": "Wednesday",
        "celestial_body": "Mercury",
        "color": "green",
        "note": "Mi",
        "cause": "Biodiversity",
    },
    3: {
        "muse": "Thunor",
        "day_name": "Thursday",
        "celestial_body": "Jupiter",
        "color": "yellow",
        "note": "Do",
        "cause": "Renewable Energy",
    },
    4: {
        "muse": "Shukra",
        "day_name": "Friday",
        "celestial_body": "Venus",
        "color": "blue",
        "note": "La",
        "cause": "Well-being",
    },
    5: {
        "muse": "Dosei",
        "day_name": "Saturday",
        "celestial_body": "Saturn",
        "color": "purple",
        "note": "Fa",
        "cause": "Zero Hunger",
    },
    6: {
        "muse": "Solis",
        "day_name": "Sunday",
        "celestial_body": "Sun",
        "color": "orange",
        "note": "So",
        "cause": "Human Rights",
    },
}


def initialize_tables():
    """Initialize database tables with sample data if needed"""
    db = get_db()
    tables = db.tables()

    logger.info(f"Checking tables in database: {tables}")

    # If daily_facts table is missing, create it with a test record
    if "daily_facts" not in tables:
        logger.warning("daily_facts table not found, initializing with test data")
        current_date = datetime.now()
        day_info = get_muse_for_today()

        # Create test fact
        test_fact = {
            "date": current_date.strftime("%Y-%m-%d"),
            "muse": day_info["muse"],
            "day_of_week": day_info["day_name"],
            "celestial_body": day_info["celestial_body"],
            "color": day_info["color"],
            "note": day_info["note"],
            "social_cause": day_info["cause"],
            "kingdoms_life_subject": "Test Organism",
            "fun_fact": "This is a test fact automatically generated during initialization.",
            "question_asked": "How can we make the world better today?",
            "fact_check_link": "https://example.com",
            "created_at": current_date.isoformat(),
        }

        doc_id = insert_with_logging("daily_facts", test_fact)
        logger.info(f"Created test fact with ID {doc_id}")
        return True

    return False


def get_muse_for_today():
    """Get the muse information for today's day of the week"""
    day_of_week = datetime.now().weekday()  # 0 is Monday, 6 is Sunday
    return MUSES.get(day_of_week)


def check_fact_exists(date: datetime) -> bool:
    """Check if a fact already exists for the given date"""
    try:
        Facts = Query()
        date_str = date.strftime("%Y-%m-%d")
        logger.info(f"Checking if fact exists for date: {date_str}")

        fact = get_with_logging("daily_facts", Facts.date == date_str)
        return fact is not None
    except Exception as e:
        logger.error(f"Error checking for existing fact: {e}")
        return False


def generate_fun_fact(day_info: dict, used_kingdom_life: list) -> FunFactModel:
    """Generate a fun fact using OpenAI API"""
    prompt = f"""Generate a fascinating and scientifically accurate fun fact about an organism in the five kingdom's of life that relates to {day_info['cause']}.

    'fun_fact':
    - Focused on the organism and its unique adaptations or behaviors
    - Be 2 max 3 sentences in length
    - Be appropriate for general audiences
    - 'question_asked': The provoking question separated out. Is a thought-provoking question that encourages readers to consider how this natural adaptation might inspire sustainable transformation or innovation.
            Make the question engaging and actionable for the user that reads. Don't repeat the fun fact in the question, but rather ask something that relates to the fun fact and the cause of the day. Be less than a sentence short
    - 'fact_check_link: include a fact check for this information by giving me an URL that:
        - Points to a reliable, up-to-date, and accessible webpage
        - Is from an authoritative organization (e.g., WWF, IUCN, National Geographic, academic or government sites)
        - Is not a generic homepage, redirect page, or one that returns a "Page not found" or has no detailed content
        - Avoids broken or placeholder links (e.g., check that the page contains information directly related to the fun fact)

    Today is {day_info['day_name']}, associated with {day_info['celestial_body']}, the color {day_info['color']}, and relates to {day_info['cause']}. The kingdoms_life_subject MUST NOT be one of this list {used_kingdom_life}

    Return the response in JSON format with two fields:
    1. 'kingdoms_life_subject': A brief name of the species or organism (1-3 words)
    2. 'fun_fact': The complete fun fact as described above
    3. 'question_asked': The provoking question created
    4. 'fact_check_link': The ecosia search bar prefilled with the fact, used to validate and check

    JSON format:
    {{
      "kingdoms_life_subject": "Species name",
      "fun_fact": "The complete fun fact text here."
      "question_asked": "The provoking question created"
      "fact_check_link": "The ecosia search prefilled fact check, shorten to 5 words the subject and the fact to pre-populate the seach bar of ecosia, return a full URL to ecosia with it"
    }}
    """

    try:
        logger.info(
            f"Generating fun fact for {day_info['muse']} about {day_info['cause']}"
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a biology or natural scientist expert specializing in fascinating kingdom's of life facts related to environmental and social causes. Answer only in JSON format as specified.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        logger.info(
            f"🌌 [OpenAI] Fun fact generated for muse '{day_info['muse']}' | Prompt length: {len(prompt)} | Response chars: {len(result_text)}"
        )
        return FunFactModel(**result)
    except Exception as e:
        logger.error(f"☄️ [OpenAI] Error generating fun fact: {e}")
        return FunFactModel(
            kingdoms_life_subject="Default organism",
            fun_fact="Due to technical issues, today's fact couldn't be generated. Please check back tomorrow for a new inspiration from nature.",
            question_asked="nd",
            fact_check_link="nd",
        )


def get_used_kingdom_life(muse: str) -> list:
    """
    Returns a list of distinct kingdoms_life_subject associated with the given muse.
    """
    try:
        Facts = Query()
        logger.info(f"Getting used kingdom life subjects for muse: {muse}")

        # Use search with logging to get all facts for this muse
        results = search_with_logging("daily_facts", Facts.muse == muse)

        # Extract distinct kingdoms_life_subject values
        kingdoms_life_set = {item.get("kingdoms_life_subject", "") for item in results}
        kingdoms_life_list = list(filter(None, kingdoms_life_set))

        logger.info(
            f"Found {len(kingdoms_life_list)} existing kingdom life subjects for {muse}"
        )
        return kingdoms_life_list

    except Exception as e:
        logger.error(f"Error retrieving kingdom's of life: {e}")
        return []


def store_fun_fact(date: datetime, day_info: dict, fact_info: FunFactModel):
    """Store the generated fun fact in the database"""
    logger.info(
        f"📝 [DB] Storing fun fact for muse '{day_info['muse']}' on {date.strftime('%Y-%m-%d')}"
    )

    # Check if we already have a fact for today
    Facts = Query()
    existing_fact = get_with_logging(
        "daily_facts", Facts.date == date.strftime("%Y-%m-%d")
    )

    if existing_fact:
        logger.info(
            f"Fun fact for {date.strftime('%Y-%m-%d')} already exists. Skipping."
        )
        return

    # Create the data structure
    fact_data = {
        "date": date.strftime("%Y-%m-%d"),
        "muse": str(day_info["muse"]),
        "day_of_week": day_info["day_name"],
        "celestial_body": day_info["celestial_body"],
        "color": day_info["color"],
        "note": day_info["note"],
        "social_cause": day_info["cause"],
        "kingdoms_life_subject": fact_info.kingdoms_life_subject,
        "fun_fact": fact_info.fun_fact,
        "question_asked": fact_info.question_asked,
        "fact_check_link": fact_info.fact_check_link,
        "created_at": datetime.now().isoformat(),
    }

    # Insert with logging
    insert_with_logging("daily_facts", fact_data)

    logger.info(f"🌠 [DB] Fun fact for muse '{day_info['muse']}' successfully stored!")


def main():
    """Main function to generate and store daily fun fact"""
    current_date = datetime.now()
    logger.info(f"Generating fact for date: {current_date.strftime('%Y-%m-%d')}")

    # Check database status
    db = get_db()
    tables = db.tables()
    logger.info(f"Database contains tables: {tables}")

    # Initialize tables if needed
    initialized = initialize_tables()
    if initialized:
        logger.info("Database tables initialized with test data")
        # If we just initialized the tables, we can exit as we've already created a fact
        return

    if check_fact_exists(current_date):
        logger.info(
            f"🌑 [DB] Fact for {current_date.strftime('%Y-%m-%d')} already exists. Exiting."
        )
        return

    day_info = get_muse_for_today()
    logger.info(f"Today's muse is {day_info['muse']} for {day_info['cause']}")

    used_kingdom_life = get_used_kingdom_life(day_info["muse"])
    logger.info(
        f"✨ [OpenAI] Generating fun fact for muse '{day_info['muse']}' ({day_info['cause']}) avoiding {used_kingdom_life} ..."
    )
    fact_info = generate_fun_fact(day_info, used_kingdom_life)

    store_fun_fact(current_date, day_info, fact_info)
    logger.info(
        f"🌌 [OpenAI] Successfully generated and stored fun fact about {fact_info.kingdoms_life_subject}"
    )
    logger.info(f"🌟 [OpenAI] Fun fact: {fact_info.fun_fact}")
    logger.info(f"❓ [OpenAI] and question asked: {fact_info.question_asked}")


if __name__ == "__main__":
    main()
