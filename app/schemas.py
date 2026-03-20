from pydantic import BaseModel
from typing import List, Optional


class TopPrediction(BaseModel):
    disease: str
    confidence: float


class ImagePrediction(BaseModel):
    top3: List[TopPrediction]
    uncertainty: float
    action: str
    questions: Optional[List[str]]


class AnswerRequest(BaseModel):
    disease: str
    image_conf: float
    answers: List[str]


class FinalPrediction(BaseModel):
    disease: str
    fused_confidence: float
    decision: str