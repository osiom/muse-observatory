import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to OpenAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_project_response(user_paragrph, fact_info):
    """
    Given a user's paragraph, an animal_subject, and a thought-provoking question,
    use OpenAI to generate three real-world environmental or sustainability-related
    projects that connect the user's ideas to the natural adaptation of the organism.
    
    Returns: List of 3 projects in JSON format, each with:
        - 'project_name'
        - 'organization'
        - 'geographic_level': one of ["global", "national", "regional", "local"]
    """
    print(f"Connecting to OpenAI to fetch projects for: {fact_info['animal_subject']}")

    prompt = f"""
        Based on the following user reflection or idea:

        \"\"\"{user_paragrph}\"\"\"

        And inspired by the organism \"{fact_info['animal_subject']}\" and the question:

        \"\"\"{fact_info['question_asked']}\"\"\"

        Find 3 real-world projects or initiatives from around the world that are relevant to what the user is thinking about, and that show a meaningful connection between this natural adaptation and efforts in sustainability, conservation, or innovation.

        Each project should:
        - Be latest updated with the reference and URL links
        - Be a real and specific initiative (no made-up projects)
        - Be linked to the general topic discussed in the paragraph and the natural world example
        - Search and prefer more detailed and localised projects instead of big ones
        - Include the project's name, the organization running it, and its geographic level: one of [global, national, regional, local]

        Return ONLY a JSON object in the following format:

        {{
        "projects": [
            {{
            "project_name": "Name of the project",
            "organization": "Organization running it",
            "geographic_level": "global | national | regional | local"
            "link_to_organization" "URL link to the organization"
            }},
            ...
        ]
        }}
    """
    print(f"Generating results...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are an environmental research assistant trained in sustainable development projects. Return only factual, real-world examples. Answer strictly in the provided JSON format."
                },
                {"role": "user", "content": prompt}
            ]
        )
        print(f"Generating results...")
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        print(f"Found results and returning {result}")
        return result

    except Exception as e:
        print(f"Error generating related projects: {e}")
        return {}
    
def main():
    """Main function to generate and store daily fun fact"""
    user_paragrph = "Scientific research for sea floors can use the same tool or something similar to the sponge"
    fact_info = {
        "animal_subject": "Bottlenose dolphins",
        "question_asked": "How might the tool-using behavior of organism like bottlenose dolphins inspire innovative approaches to preserving marine ecosystem?"
    }
    get_project_response(user_paragrph, fact_info)


if __name__ == "__main__":
    main()