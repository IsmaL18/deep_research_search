from pydantic import BaseModel
from typing import List

class ReasoningOutputFormat(BaseModel):
    action: str

class GapQuestionsGenerationOutputFormat(BaseModel):
    gap_questions: List[str]