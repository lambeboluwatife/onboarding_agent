from pydantic import BaseModel

class TaskOutput(BaseModel):
    name: str
    value: str
