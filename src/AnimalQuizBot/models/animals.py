from pydantic import BaseModel, RootModel


class Animal(BaseModel):
    name: str
    emoji: str
    description: str
    custody: str
    image: str

class AnimalsData(RootModel[dict[str, Animal]]):
    pass