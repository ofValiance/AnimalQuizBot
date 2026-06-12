from pathlib import Path
import asyncio
from pydantic.v1 import ValidationError

from src.AnimalQuizBot.models.reviews import Review, Reviews
from src.AnimalQuizBot.models.quiz import QuizData
from src.AnimalQuizBot.models.animals import AnimalsData


class DataLoader:
    def __init__(self, resources_path: Path):
        self.RESOURCES_PATH = resources_path
        self.lock = asyncio.Lock()
        self.IMAGES_PATH = self.RESOURCES_PATH / "images"

    def load_quiz(self, quiz_json: str) -> QuizData:
        try:
            json_str = (self.RESOURCES_PATH / quiz_json).read_text(encoding="utf-8")
            print("Quiz data loaded")
            return QuizData.model_validate_json(json_str)
        except ValidationError as e:
            print(f"JSON validation error: {e}")
            raise
        except FileNotFoundError:
            print(f"No {quiz_json} file found")
            raise

    def load_animals(self, animals_json: str) -> AnimalsData:
        try:
            json_str = (self.RESOURCES_PATH / animals_json).read_text(encoding="utf-8")
            print("Animals data loaded")
            return AnimalsData.model_validate_json(json_str)
        except ValidationError as e:
            print(f"JSON validation error: {e}")
            raise
        except FileNotFoundError:
            print(f"No {animals_json} file found")
            raise

    async def download_review(self, review: Review, reviews_json: str):
        async with self.lock:
            try:
                json_str = (self.RESOURCES_PATH / reviews_json).read_text(encoding="utf-8")
                reviews = Reviews.model_validate_json(json_str)
                reviews.root.append(review)
                json_output = reviews.model_dump_json(ensure_ascii=False)
                Path(self.RESOURCES_PATH / reviews_json).write_text(json_output, encoding="utf-8")
                print("Review saved")
            except ValidationError as e:
                print(f"JSON validation error: {e}")
                raise
            except FileNotFoundError:
                print(f"No {reviews_json} file found")
                raise