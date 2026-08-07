import os
from ..core.config import settings
import logging 
from typing import Optional
from anthropic import Anthropic
from ..models.pipeline_state import PipelineState
from ..core.config import settings
import json

logger = logging.getLogger(__name__)
client = Anthropic(api_key=settings.ANTHROPIC_KEY)


template_path = os.path.join(os.path.dirname(__file__), "../templates/profile_template.md")
base_template_path = os.path.join(os.path.dirname(__file__), "../prompts/base_system_prompt.md")
with open(template_path, "r") as f:
    profile_template = f.read()
with open(base_template_path, "r") as f:
    base_template = f.read()

def cv_parser(state: PipelineState) -> dict:
    """
    Parse CV text into structured JSON
    IP: state["cv_raw"], state["session_id"]
    OP: state["cv_parsed"], state["missing_fields"], state["erros"]
    """
    
    try:
        cv_raw = state.get("cv_raw")
        
        prompt = f"""
        You are a resume parser. Extract information form the resume below and 
        structure it following this profile template:
        
        {profile_template}
        
        Return a JSON object with two fields: 
        1. "cv_parsed ": The structured profile (using the template as reference for field names and structure)
        2. "missing_fields": List of mandatory fields that are NOT in the resume
        Mandatory fields:
        - personal_info.name
        - personal_info.email
        - education (at least 1 entry)
        - work_experience (at least 1 entry)
        - skills.hard_skills
        - skills.soft_skills
        
        Resume to parse: 
        {cv_raw}
        
        Return ONLY valid JSON. No markdown, no extra text.
        """
        
        message = client.messages.create(
            model="claude-opus-4-1",
            max_tokens=3000,
            system=base_template,
            messages=[
                {'role':'user', 'content':prompt}
            ]
        )
        
        response_text = message.content[0].text
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        response_json = json.loads(response_text)
        cv_parsed = response_json.get("cv_parsed", {})
        missing_fields = response_json.get("missing_fields", [])
        
        data_dir = os.path.join(os.path.dirname(__file__), "../../data/user_profile")
        os.makedirs(data_dir, exist_ok=True)
        
        cv_parsed_path = os.path.join(data_dir, "cv_parsed.json")
        with open(cv_parsed_path, "w") as f:
            json.dump(cv_parsed, f, indent=2)
        
        logger.info(f"CV parsed and saved to {cv_parsed_path}")
        
        return {
            "cv_parsed": cv_parsed,
            "missing_fields": missing_fields,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"JSON parse error {e}")
        return {"error": f"CV parsing error {str(e)}"}
    