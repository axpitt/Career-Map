from pydantic import BaseModel, Field
from typing import List, Literal


class CareerAnalysisResponse(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Resume score from 0 to 100")
    level: Literal["Beginner", "Intermediate", "Strong"] = Field(
        ..., description="Career level based on resume analysis"
    )
    strengths: List[str] = Field(..., description="List of resume strengths")
    weaknesses: List[str] = Field(..., description="List of resume weaknesses")
    companies_to_apply: List[str] = Field(
        ..., description="Companies to apply to based on current level and city"
    )
    upgrade_target_companies: List[str] = Field(
        ..., description="Companies to target after skill upgrade"
    )
    upgrade_requirements: List[str] = Field(
        ..., description="Skills and steps required to reach the next level"
    )
