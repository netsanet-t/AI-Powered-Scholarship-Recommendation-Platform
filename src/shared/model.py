from pydantic import BaseModel, Field
from typing import Annotated

class Parameters(BaseModel):
    limit: Annotated[int, Field(10, le=50)]
    offset: Annotated[int, Field(0, ge=0)]