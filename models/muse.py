import uuid
from typing import Dict, Any
from datetime import datetime
from typing import Dict, Any, List
from psycopg2.extras import RealDictCursor
from config.db import get_db_connection, return_db_connection
from logger import get_logger

logger = get_logger(__name__)


CHART = {
    "lunes": {
        "color": "#5783A6",
        "support_color": "#3B75A4",
        "astro_color": "#FBFBFB",
        "name": "Lunes"
    },
    "ares": {
        "color": "#D54D2E",
        "support_color": "#C45C44",
        "astro_color": "#000000",
        "name": "Ares"
    },
    "rabu": {
        "color": "#8CB07F",
        "support_color": "#BDEDAB",
        "astro_color": "#000000",
        "name": "Rabu"
    },
    "thunor": {
        "color": "#F8D86A",
        "support_color": "#F6DE90",
        "astro_color": "#FBFBFB",
        "name": "Thunor"
    },
    "shukra": {
        "color": "#5E47A1",
        "support_color": "#1F1427",
        "astro_color": "#FBFBFB",
        "name": "Shukra"
    },
    "dosei": {
        "color": "#7F49A2",
        "support_color": "#4C315E",
        "astro_color": "#FBFBFB",
        "name": "Dosei"
    },
    "solis": {
        "color": "#D48348",
        "support_color": "#F2AF7E",
        "astro_color": "#000000",
        "name": "Solis"
    },
    "solis": {
        "color": "#FFFFFF",
        "support_color": "#FFFFFF",
        "astro_color": "#000000",
        "name": "Cocoex"
    },    
}

class Oracle:
    def __init__(self):
        logger.info("Initiating the Oracle of the day")
        fact = Oracle.get_todays_fact()

        logger.info("Understanding to which Muse are we connected today")
        self.daily_muse = fact.get("muse", "cocoex")
        logger.info(f"Muse of the day: {self.daily_muse}")
        self.social_cause = fact.get("social_cause", "Unknown")
        logger.info(f"for: {self.social_cause}")
        self.fun_fact = fact.get("fun_fact", "No fact today.")
        self.question_asked = fact.get("question_asked", "No question asked.")
        self.fact_check_link = fact.get("fact_check_link", "#")
        
        self.color = CHART.get(self.daily_muse.lower(), {}).get("color", "#FFFFFF")
        self.support_color = CHART.get(self.daily_muse.lower(), {}).get("support_color", "#FFFFFF")
        self.astro_color = CHART.get(self.daily_muse.lower(), {}).get("astro_color", "#FFFFFF")
        self.muse_name = CHART.get(self.daily_muse.lower(), {}).get("name")
    
    @staticmethod
    def get_todays_fact() -> Dict[str, Any]:
        """Fetch today's fact from database"""
        conn = None
        cursor = None
        logger.info("Fetching today's fact from db")
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("SELECT * FROM daily_facts WHERE date = %s", (today,))
            return cursor.fetchone() or {
                'muse': 'cocoex',
                'social_cause': 'cocoex',
                'fun_fact': 'The oracle didnt answer today!',
                'question_asked': 'What is the meaning of life?',
                'fact_check_link': '#'
            }
            logger.info("Fetch for today's facto completed.")
        except Exception as e:
            logger.error(f"Database error: {e}")
            return {
                'muse': 'cocoex',
                'social_cause': 'Database Error',
                'fun_fact': 'Could not fetch fact today',
                'question_asked': 'Try again later?',
                'fact_check_link': '#'
            }
        finally:
            if cursor:
                cursor.close()
            if conn:
                return_db_connection(conn)

    def save_inspiration(self, user_input: str, projects: List[Dict]):
        """Save user inspiration and projects"""
        conn = None
        cursor = None
        logger.info("Saving inspiration provided by the observer.")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            inspiration_id = str(uuid.uuid4())
            logger.info("Inserting data into database...")
            cursor.execute("""
                INSERT INTO inspirations 
                (date, id, day_of_week, social_cause, muse, user_inspiration)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    datetime.now().date(),
                    inspiration_id,
                    datetime.now().strftime('%A'),
                    self.social_cause,
                    self.muse_name,
                    user_input
                ))
            logger.info("Inserting data into database...")
            logger.info("Inserting projects into database...")
            for project in projects:
                logger.info(f"Inserting project: {project['project_name']}")
                cursor.execute("""
                    INSERT INTO projects 
                    (id, project_name, organisation, geographical_level, 
                    link_to_organisation, sk_inspiration)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        str(uuid.uuid4()),
                        project['project_name'],
                        project['organization'],
                        project['geographic_level'],
                        project['link_to_organization'],
                        inspiration_id
                    ))
                logger.info(f"Inserting completed.")
            conn.commit()
        except Exception as e:
            logger.error(f"Save failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                return_db_connection(conn)
