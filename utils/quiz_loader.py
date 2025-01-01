import json
from typing import List, Dict

def load_questions(file_path: str) -> List[Dict]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Загружаем вопросы
ALL_QUESTIONS = load_questions("question.json")