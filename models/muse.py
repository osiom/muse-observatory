import uuid
from datetime import datetime
from typing import Any, Dict, List

from tinydb import Query

from db.db import get_db_connection, return_db_connection
from models.schemas import InspirationModel, ProjectModel
from utils.logger import get_logger

logger = get_logger(__name__)


CHART = {
    "lunes": {
        "color": "#5783A6",
        "support_color": "#3B75A4",
        "astro_color": "#FBFBFB",
        "name": "Lunes",
    },
    "ares": {
        "color": "#D54D2E",
        "support_color": "#C45C44",
        "astro_color": "#FBFBFB",
        "name": "Ares",
    },
    "rabu": {
        "color": "#8CB07F",
        "support_color": "#BDEDAB",
        "astro_color": "#FBFBFB",
        "name": "Rabu",
    },
    "thunor": {
        "color": "#F8D86A",
        "support_color": "#F6DE90",
        "astro_color": "#FBFBFB",
        "name": "Thunor",
    },
    "shukra": {
        "color": "#5E47A1",
        "support_color": "#1F1427",
        "astro_color": "#FBFBFB",
        "name": "Shukra",
    },
    "dosei": {
        "color": "#7F49A2",
        "support_color": "#4C315E",
        "astro_color": "#FBFBFB",
        "name": "Dosei",
    },
    "solis": {
        "color": "#D48348",
        "support_color": "#F2AF7E",
        "astro_color": "#FBFBFB",
        "name": "Solis",
    },
    "cocoex": {
        "color": "#000000",
        "support_color": "#626262",
        "astro_color": "#FBFBFB",
        "name": "Cocoex",
    },
}


class Oracle:
    def __init__(self: "Oracle"):
        logger.info(
            "🌌 Initiating the Oracle of the day — tuning into the cosmic frequencies..."
        )
        fact = Oracle.get_todays_fact()

        logger.info("✨ Seeking which Muse is guiding us through the universe today...")
        self.daily_muse = fact.get("muse", "cocoex")
        logger.info(f"🌠 Muse of the day: {self.daily_muse}")
        self.social_cause = fact.get("social_cause", "Unknown")
        logger.info(f"🌍 Social cause in focus: {self.social_cause}")
        self.fun_fact = fact.get("fun_fact", "No fact today.")
        self.question_asked = fact.get("question_asked", "No question asked.")
        self.fact_check_link = fact.get("fact_check_link", "#")

        muse_chart = CHART.get(self.daily_muse.lower(), {})
        self.color = muse_chart.get("color", "#FFFFFF")
        self.support_color = muse_chart.get("support_color", "#FFFFFF")
        self.astro_color = muse_chart.get("astro_color", "#FFFFFF")
        self.muse_name = muse_chart.get("name")
        logger.info(
            f"🎨 Muse colors: {self.color}, {self.support_color}, {self.astro_color}"
        )

    @staticmethod
    def get_todays_fact() -> Dict[str, Any]:
        """Fetch today's fact from the cosmic database"""
        logger.info("🔮 Fetching today's fact from the cosmic archives...")
        try:
            db = get_db_connection()
            today = datetime.now().strftime("%Y-%m-%d")
            Facts = Query()
            fact = db.table("daily_facts").get(Facts.date == today)

            if fact:
                logger.info("🌟 Fact found for today — the universe speaks!")
                return fact
            else:
                logger.warning("🌑 No fact found for today — the stars are silent.")
                return {
                    "muse": "cocoex",
                    "social_cause": "cocoex",
                    "fun_fact": "The oracle didn't answer today!",
                    "question_asked": "What is the meaning of life?",
                    "fact_check_link": "#",
                }
        except Exception as e:
            logger.error(f"☄️ Database error in the cosmic archives: {e}")
            return {
                "muse": "cocoex",
                "social_cause": "Database Error",
                "fun_fact": "Could not fetch fact today",
                "question_asked": "Try again later?",
                "fact_check_link": "#",
            }

    def save_inspiration(self: "Oracle", user_input: str, projects: List[dict]):
        """Save user inspiration and projects to the cosmic ledger"""
        # Validate input using Pydantic
        inspiration = InspirationModel(
            user_input=user_input,
            projects=[ProjectModel(**p) for p in projects],
        )
        logger.info(
            f"📝 Saving inspiration from the observer to the cosmic ledger for muse {self.muse_name}..."
        )
        try:
            db = get_db_connection()
            inspiration_id = str(uuid.uuid4())

            # Insert inspiration
            logger.info("🌌 Inserting inspiration into the database...")
            db.table("inspirations").insert(
                {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "id": inspiration_id,
                    "day_of_week": datetime.now().strftime("%A"),
                    "social_cause": self.social_cause,
                    "muse": self.muse_name,
                    "user_inspiration": inspiration.user_input,
                    "created_at": datetime.now().isoformat(),
                }
            )

            # Insert projects
            logger.info("🌠 Inserting related projects into the cosmic registry...")
            for project in inspiration.projects:
                logger.info(
                    f"🚀 Inserting project: {project.project_name} (by {project.organization})"
                )
                db.table("projects").insert(
                    {
                        "id": str(uuid.uuid4()),
                        "project_name": project.project_name,
                        "organisation": project.organization,
                        "geographical_level": project.geographic_level,
                        "link_to_organisation": project.link_to_organization,
                        "sk_inspiration": inspiration_id,
                        "created_at": datetime.now().isoformat(),
                    }
                )

            logger.info(
                f"🌌 Inspiration and projects for muse {self.muse_name} have been committed to the universe!"
            )
        except Exception as e:
            logger.error(f"💥 Save failed in the cosmic ledger: {str(e)}")
            raise
