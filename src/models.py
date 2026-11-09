from pydantic import BaseModel, Field


class Employee(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(gt=0)
