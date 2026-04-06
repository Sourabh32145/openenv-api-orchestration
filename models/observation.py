from pydantic import BaseModel
from typing import List, Dict, Optional

class Observation(BaseModel):
    pending_tasks: List[str]
    completed_tasks: List[str]
    api_status: Dict[str, str]
    last_error: Optional[str]
    step_count: int
