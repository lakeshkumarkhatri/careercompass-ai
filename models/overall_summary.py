from pydantic import BaseModel

class OverallSummary(BaseModel):
    """Overall summary model."""
    overall_summary: str
