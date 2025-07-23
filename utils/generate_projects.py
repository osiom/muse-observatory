import json
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from openai import AsyncOpenAI  # Changed to async
from tinydb import Query

from db.db import get_db, insert_with_logging, search_with_logging
from models.muse import Oracle
from utils.logger import get_logger

# Create a logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

# Connect to OpenAI API
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=60)  # Async client

# --- OpenAI Token Quota Config ---
DAILY_TOKEN_QUOTA = 100_000  # Set your daily quota here


async def check_and_increment_token_quota(tokens_used: int) -> bool:
    """
    Check if the daily quota is exceeded based on the usage log.
    No need to update a separate table as we'll calculate totals from the log.
    """
    if tokens_used <= 0:
        return True

    current_usage = await get_current_token_usage()
    total = current_usage + tokens_used

    if total > DAILY_TOKEN_QUOTA:
        logger.warning(
            f"🚫 [Quota] Attempted to use {tokens_used} tokens, but quota ({DAILY_TOKEN_QUOTA}) would be exceeded. Current: {current_usage}"
        )
        return False

    logger.info(
        f"🔄 [Quota] Token usage within limits: {current_usage} + {tokens_used} = {total}/{DAILY_TOKEN_QUOTA}"
    )
    return True


async def log_openai_usage(
    endpoint: str, tokens_used: int, model: str, status: str, error: str = None
):
    """Log OpenAI API usage for monitoring and auditing."""
    try:
        # Insert a log entry with timestamp including date for easy filtering by date
        usage_data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "endpoint": endpoint,
            "tokens_used": tokens_used,
            "model": model,
            "status": status,
            "error": error,
        }

        # Use the helper function to insert with logging
        insert_with_logging("openai_usage_log", usage_data)

        logger.info(
            f"Logged OpenAI API usage: {endpoint}, {tokens_used} tokens, status: {status}"
        )
    except Exception as e:
        logger.error(f"Failed to log OpenAI usage: {e}")


async def get_current_token_usage() -> int:
    """
    Get the current total tokens used today from the usage log.
    This replaces the need for a separate token_usage table.
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")

        # Use the search helper to find all logs for today
        Usage = Query()
        logs = search_with_logging("openai_usage_log", Usage.date == today)

        # Sum tokens from successful calls
        total = sum(
            log.get("tokens_used", 0) for log in logs if log.get("status") == "success"
        )

        logger.info(f"Current token usage for today ({today}): {total}")
        return total
    except Exception as e:
        logger.error(f"Error getting current token usage: {e}")
        return 0


async def get_project_response(oracle_day: Oracle, user_paragraph: str):  # Added async
    """
    Given a fact_info dictionary and a user's paragraph,
    use OpenAI to generate three real-world environmental or sustainability-related
    projects that connect the user's ideas to the natural adaptation of the organism.
    """
    logger.debug("get_project_response called")

    if not isinstance(oracle_day, Oracle):
        logger.error("No Oracle has been assigned today")
        return {"projects": []}

    prompt = f"""
    Based on this user reflection:
    \"\"\"{user_paragraph}\"\"\"

    And inspired by {oracle_day.muse_name} and the question:
    \"\"\"{oracle_day.question_asked}\"\"\"

    Find 3 real, specific projects that connect these ideas to sustainability efforts.
    Each project must:
    - Be real and verifiable
    - Include name, organization, geographic level (global/national/regional/local)
    - Have a working URL for the organization specific you found
    - Relate to both the user's ideas and the muse's theme

    Return only valid JSON, without any Markdown formatting or triple backticks, format with schema:
    {{
        "projects": [
            {{
                "project_name": "...",
                "organization": "...",
                "geographic_level": "...",
                "link_to_organization": "..."
            }}
        ]
    }}
    """

    # --- Pre-check quota before making OpenAI call ---
    ESTIMATED_MAX_TOKENS = 2048  # Adjust as needed for your use case
    current_tokens = await get_current_token_usage()
    if current_tokens + ESTIMATED_MAX_TOKENS > DAILY_TOKEN_QUOTA:
        await log_openai_usage(
            endpoint="get_project_response",
            tokens_used=0,
            model="gpt-4o",
            status="quota_exceeded_precheck",
            error="OpenAI daily token quota would be exceeded (pre-check).",
        )
        logger.error("OpenAI daily token quota would be exceeded (pre-check).")
        return {
            "error": "OpenAI daily token quota exceeded. Please try again tomorrow."
        }
    # --- End pre-check ---
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an environmental research assistant. Return only real projects in exact JSON format.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        usage = getattr(response, "usage", None)
        tokens_used = (
            usage.total_tokens if usage and hasattr(usage, "total_tokens") else 0
        )
        logger.info(
            f"🌌 [OpenAI] User submission for muse '{getattr(oracle_day, 'muse_name', 'unknown')}' | Tokens used: {tokens_used} | Prompt length: {len(prompt)} | Model: gpt-4o"
        )
        if not await check_and_increment_token_quota(tokens_used):
            await log_openai_usage(
                endpoint="get_project_response",
                tokens_used=tokens_used,
                model="gpt-4o",
                status="quota_exceeded",
                error="OpenAI daily token quota exceeded.",
            )
            logger.error("🚫 [OpenAI] Daily token quota exceeded — cosmic gate closed!")
            return {
                "error": "OpenAI daily token quota exceeded. Please try again tomorrow."
            }
        await log_openai_usage(
            endpoint="get_project_response",
            tokens_used=tokens_used,
            model="gpt-4o",
            status="success",
        )
        raw_content = response.choices[0].message.content
        cleaned_content = re.sub(
            r"^```(?:json)?\s*|\s*```$", "", raw_content.strip(), flags=re.MULTILINE
        )
        result = json.loads(cleaned_content)
        logger.info(
            f"🌠 [OpenAI] Response received: {len(raw_content)} chars | Projects found: {len(result.get('projects', []))}"
        )
        logger.debug(f"🪐 [OpenAI] Project details: {result}")
        return result
    except json.JSONDecodeError as e:
        await log_openai_usage(
            endpoint="get_project_response",
            tokens_used=0,
            model="gpt-4o",
            status="json_error",
            error=str(e),
        )
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Raw response: {response.choices[0].message.content}")
        return {"projects": []}
    except Exception as e:
        await log_openai_usage(
            endpoint="get_project_response",
            tokens_used=0,
            model="gpt-4o",
            status="error",
            error=str(e),
        )
        logger.error(f"Error generating projects: {str(e)}")
        return {"projects": []}
