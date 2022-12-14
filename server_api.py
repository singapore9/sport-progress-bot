import time

import requests

from constants import API_URL
from messages import AvailableLanguagesEnum


def send_activity(user_id, activity_name, iterations_count, pause_before_item):
    r = requests.post(f"{API_URL}/api/workout-item/", json={
        "name": activity_name,
        "iterations_count": iterations_count,
        "pause_before_item": pause_before_item,
        "timestamp": int(time.time()),
        "user_id": str(user_id),
    })
    return r.status_code == 200


def get_exercises(language: AvailableLanguagesEnum):
    r = requests.get(f"{API_URL}/api/exercise/translate/{language.name}")
    exercises = []
    if r.status_code == 200:
        exercises = r.json()['list'][0]
    return exercises


def send_exercise(exercise_name):
    r = requests.post(f"{API_URL}/api/exercise/", data={
        "name": exercise_name
    })
    return r.status_code == 200


def get_user_language(user_id):
    r = requests.get(f"{API_URL}/api/language/{user_id}")
    language = None
    if r.status_code == 200:
        language = r.json()['language']
        try:
            language = AvailableLanguagesEnum[language]
        except Exception as _:
            language = None
    if language is None:
        language = AvailableLanguagesEnum.eng
    return language


def set_user_language(user_id, language: AvailableLanguagesEnum):
    r = requests.post(f"{API_URL}/api/language/{user_id}", data={
        "language": language.name
    })
    return r.status_code == 200
