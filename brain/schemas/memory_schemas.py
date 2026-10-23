from pydantic import BaseModel 
from datetime import datetime

class InferenceSchema(BaseModel):
    id: str
    command: str 
    state_embedding: list[float]
    action_id: int 
    log_prob: float 
    critic_value: float 
    reward: float
    timestamp: datetime