import requests

from constants import API_URL


def send_activity(activity_name, iterations_count, pause_before_item):
    r = requests.post(f"{API_URL}/api/workout-item/", json={
        "name": activity_name,
        "iterations_count": iterations_count,
        "pause_before_item": pause_before_item
    })
    return r.status_code == 200


def get_exercises():
    r = requests.get(f"{API_URL}/api/exercise/")
    exercises = []
    if r.status_code == 200:
        exercises = r.json()['list'][0]
    return exercises


def send_exercise(exercise_name):
    r = requests.post(f"{API_URL}/api/exercise/", data={
        "name": exercise_name
    })
    return r.status_code == 200
