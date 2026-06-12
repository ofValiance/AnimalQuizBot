from pathlib import Path
from src.AnimalQuizBot.data.loader import DataLoader

dl = DataLoader(Path(__file__).parent.parent.parent.parent / "resources")

QUIZ_DATA = dl.load_quiz("quiz.json")
ANIMALS_DATA = dl.load_animals("animals.json")
IMAGES_PATH = dl.IMAGES_PATH

__all__ = [dl, "QUIZ_DATA", "ANIMALS_DATA", "IMAGES_PATH"]