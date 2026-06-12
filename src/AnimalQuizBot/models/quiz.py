from pydantic import BaseModel


class Option(BaseModel):
    id: int
    emoji: str
    text: str
    scores: dict[str, int]

class Question(BaseModel):
    id: int
    text: str
    options: list[Option]

class QuizData(BaseModel):
    questions: list[Question]