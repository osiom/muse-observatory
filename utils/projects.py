import os
import re
import json
from openai import AsyncOpenAI  # Changed to async
from dotenv import load_dotenv
from logger import get_logger

from models.muse import Oracle

# Create a logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

# Connect to OpenAI API
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=60)  # Async client

async def get_project_response(oracle_day: Oracle, user_paragraph):  # Added async
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
    - Have a working URL
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
    
    try:
        response = await client.chat.completions.create(  # Added await
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an environmental research assistant. Return only real projects in exact JSON format."
                },
                {"role": "user", "content": prompt}
            ]
        )
        logger.info(f"Received raw response: {response.choices[0].message.content}")
        raw_content = response.choices[0].message.content
        cleaned_content = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_content.strip(), flags=re.MULTILINE)

        result = json.loads(cleaned_content)
        logger.debug(f"Found {len(result.get('projects', []))} projects")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Raw response: {response.choices[0].message.content}")
        return {"projects": []}
    except Exception as e:
        logger.error(f"Error generating projects: {str(e)}")
        return {"projects": []}