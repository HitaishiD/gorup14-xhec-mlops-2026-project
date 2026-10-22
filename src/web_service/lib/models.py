# Pydantic models for the web service

from typing import Literal

from pydantic import BaseModel


class AbaloneFeatures(BaseModel):
    sex: Literal["M", "F", "I"]
    length: float
    diameter: float
    height: float
    whole_weight: float
    shucked_weight: float
    viscera_weight: float
    shell_weight: float


class Prediction(BaseModel):
    rings: float
