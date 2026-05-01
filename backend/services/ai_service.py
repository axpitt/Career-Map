import json
import logging
from openai import OpenAI
from fastapi import HTTPException
from config import settings

logger = logging.getLogger(__name__)

# Initialize OpenAI client with config
client = OpenAI(api_key=settings.openai_api_key)


def analyze_resume(resume_text: str, city: str) -> dict:
    """
    Sends extracted resume text and the user's city to OpenAI and returns
    a structured career analysis as a Python dict.
    """

    prompt = f"""You are an expert tech recruiter and career advisor.

Analyze the following resume.

User city: {city}

Return STRICT JSON ONLY in this format:

{{
  "score": <number between 0 and 100>,
  "level": "<Beginner | Intermediate | Strong>",
  "strengths": ["<strength 1>", "<strength 2>", "..."],
  "weaknesses": ["<weakness 1>", "<weakness 2>", "..."],
  "companies_to_apply": ["<company 1>", "<company 2>", "..."],
  "upgrade_target_companies": ["<company 1>", "<company 2>", "..."],
  "upgrade_requirements": ["<requirement 1>", "<requirement 2>", "..."]
}}

Rules:
- Return ONLY valid JSON. No explanation text before or after.
- Score must match level realistically:
    * Beginner: 0–40
    * Intermediate: 41–74
    * Strong: 75–100
- companies_to_apply must be real companies hiring in {city} that match the candidate's current level.
- upgrade_target_companies must be aspirational companies (e.g. FAANG, top unicorns) in or near {city}.
- upgrade_requirements must be specific, actionable steps the candidate should take.
- All lists must have between 3 and 6 items.

Resume:
{resume_text}
"""

    try:
        logger.info(f"Analyzing resume for city: {city}")

        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a career advisor AI. "
                        "You ALWAYS respond with valid JSON only. "
                        "Never include markdown, code fences, or any extra text."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=settings.openai_temperature,
            max_tokens=settings.openai_max_tokens,
        )

        raw_content = response.choices[0].message.content.strip()

        # Strip markdown code fences if model wraps JSON anyway
        if raw_content.startswith("```"):
            lines = raw_content.splitlines()
            # Remove opening fence
            lines = lines[1:] if lines[0].startswith("```") else lines
            # Remove closing fence
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            raw_content = "\n".join(lines).strip()

        analysis = json.loads(raw_content)
        logger.info(f"Successfully analyzed resume, score: {analysis.get('score')}")
        return analysis

    except json.JSONDecodeError as exc:
        logger.error(f"OpenAI returned invalid JSON: {str(exc)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI response parsing failed: {str(exc)}",
        )
    except Exception as exc:
        logger.error(f"OpenAI API error: {str(exc)}")
        raise HTTPException(
            status_code=500,
            detail="AI analysis service temporarily unavailable. Please try again later.",
        )
