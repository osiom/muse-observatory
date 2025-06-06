import os
import json
from openai import AsyncOpenAI  # Changed to async
from dotenv import load_dotenv
from logger import get_logger

# Create a logger
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

# Connect to OpenAI API
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Async client

async def get_project_response(fact_info, user_paragraph):  # Added async
    """
    Given a fact_info dictionary and a user's paragraph,
    use OpenAI to generate three real-world environmental or sustainability-related
    projects that connect the user's ideas to the natural adaptation of the organism.
    """
    logger.debug("get_project_response called")
    
    if not isinstance(fact_info, dict):
        logger.error("fact_info is not a dictionary")
        return {"projects": []}

    muse = fact_info.get('muse', 'unknown muse')
    question = fact_info.get('question_asked', 'unknown question')
    
    prompt = f"""
    Based on this user reflection:
    \"\"\"{user_paragraph}\"\"\"

    And inspired by {muse} and the question:
    \"\"\"{question}\"\"\"

    Find 3 real, specific projects that connect these ideas to sustainability efforts.
    Each project must:
    - Be real and verifiable
    - Include name, organization, geographic level (global/national/regional/local)
    - Have a working URL
    - Relate to both the user's ideas and the muse's theme

    Return JSON format with:
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
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are an environmental research assistant. Return only real projects in exact JSON format."
                },
                {"role": "user", "content": prompt}
            ]
        )
        
        result = json.loads(response.choices[0].message.content)
        logger.debug(f"Found {len(result.get('projects', []))} projects")
        return result

    except Exception as e:
        logger.error(f"Error generating projects: {str(e)}")
        return {"projects": []}