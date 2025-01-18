from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Schema para validação e criação de disponibilidade
class Availability(BaseModel):
    doctor_id: str = Field(..., description="ID do médico")
    available_times: List[datetime] = Field(..., description="Horários específicos disponíveis para o médico")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
