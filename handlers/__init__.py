from .start import register_handlers as register_start_handlers
from .quiz import register_handlers as register_quiz_handlers


def register_handlers(dp):
    register_start_handlers(dp)
    register_quiz_handlers(dp)

   
