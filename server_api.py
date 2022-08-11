import requests

from constants import API_URL


def send_activity(activity_name, iterations_count, pause_before_item):
    r = requests.post(f"{API_URL}/api/workout-item/", json={
        "name": activity_name,
        "iterations_count": iterations_count,
        "pause_before_item": pause_before_item
    })
    return r.status_code == 200
