from start import register_handlers as register_start_handlers
from quiz import register_handlers as register_quiz_handlers
from difficulty_selection import  register_handlers as register_difficulty_handlers
from main_menu import register_handlers as register_menu_handlers



def register_handlers(dp):
    register_start_handlers(dp)
    register_quiz_handlers(dp)
    register_difficulty_handlers(dp)
    register_menu_handlers(dp)


   
