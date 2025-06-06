from typing import Dict, Any
from datetime import datetime
from psycopg2.extras import RealDictCursor
from config.db import get_db_connection, return_db_connection
from logger import get_logger

logger = get_logger(__name__)

class Muse:
    COLORS = {
        "Lunes": "#5783A6",
        "Ares": "#D54D2E",
        "Rabu": "#8CB07F",
        "Thunor": "#F8D86A",
        "Shukra": "#5E47A1",
        "Dosei": "#7F49A2",
        "Solis": "#D48348"
    }

    @staticmethod
    def get_todays_fact() -> Dict[str, Any]:
        """Fetch today's fact from database"""
        conn = None
        cursor = None
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

    @staticmethod
    def save_inspiration(fact_info: Dict[str, Any], user_input: str, projects: List[Dict]):
        """Save user inspiration and projects"""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            inspiration_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO inspirations 
                (date, id, day_of_week, social_cause, muse, user_inspiration)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    datetime.now().date(),
                    inspiration_id,
                    datetime.now().strftime('%A'),
                    fact_info['social_cause'],
                    fact_info['muse'],
                    user_input
                ))
            
            for project in projects:
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
            
            conn.commit()
        except Exception as e:
            logger.error(f"Save failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                return_db_connection(conn)

    @staticmethod
    def get_color(muse_name: str) -> str:
        """Get color associated with a muse"""
        return Muse.COLORS.get(muse_name, "#7F49A2")
    