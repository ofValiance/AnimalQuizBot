from src.AnimalQuizBot.handlers import commands_handler, quiz_handler, review_handler, menu_handler


routers = [
    commands_handler.router,
    quiz_handler.router,
    review_handler.router,
    menu_handler.router,
]

__all__ = ["routers"]