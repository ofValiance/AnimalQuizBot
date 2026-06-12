import random

from src.AnimalQuizBot.data import ANIMALS_DATA, QUIZ_DATA


async def gather_scores(answers: dict) -> dict:
    scores = {animal: 0 for animal in ANIMALS_DATA.root.keys()}
    for q_id, option_id in answers.items():
        answer_scores = QUIZ_DATA.questions[q_id - 1].options[option_id - 1].scores
        for animal, score in answer_scores.items():
            scores[animal] += score
    return scores

async def pick_animal(scores: dict) -> str:
    max_score = max(scores.values())
    winners = [animal for animal, score in scores.items() if score == max_score]
    winner = random.choice(winners)
    return winner