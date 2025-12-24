from pydantic import BaseModel, Field


class Config(BaseModel):
    verbose: bool = False
    timeout: int = 30
    tags: list[str] = Field(default_factory=list)
