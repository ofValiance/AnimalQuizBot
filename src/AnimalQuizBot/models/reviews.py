from typing import Optional
from pydantic import BaseModel, RootModel, Field
from datetime import datetime


class Review(BaseModel):
    user_id: Optional[int] = Field(default = None)
    username: Optional[str] = Field(default=None)
    animal: Optional[str] = Field(default = None)
    rating: Optional[int] = Field(default = None)
    comment: Optional[str] = Field(default = None)
    timestamp: Optional[datetime] = Field(default = datetime.now())

class Reviews(RootModel[list[Review]]):
    pass