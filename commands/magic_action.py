import base64
import json
import requests
import random
import time

from constants import GITHUB_ACCOUNT_USERNAME, GITHUB_ACCESS_TOKEN, GITHUB_REPO_NAME

from telegram import Update
from telegram.ext import CallbackContext

from commands.utils.additional_params import pass_user_id, pass_language
from messages import AvailableLanguagesEnum


def push_to_github(newline, branch, token):
    change_file_endpoint = (
        f"https://api.github.com/repos/{GITHUB_ACCOUNT_USERNAME}/"
        f"{GITHUB_REPO_NAME}/contents/README.md"
    )
    data = requests.get(
        f"{change_file_endpoint}?ref={branch}",
        headers={"Authorization": f"token {token}"}
    ).json()

    sha = data['sha']
    content = base64.b64decode(data['content'].encode('utf-8')).decode('utf-8')
    content_str = f'{content}\n- {newline}'
    content = base64.b64encode(content_str.encode('utf-8'))

    message = json.dumps({
        "message": "update",
        "branch": branch,
        "content": content.decode('utf-8'),
        "sha": sha
    })

    resp = requests.put(
        change_file_endpoint, data=message,
        headers={"Content-Type": "application/json", "Authorization": f"token {token}"}
    )
    return resp


@pass_user_id
@pass_language
async def do_commits(user_id: int, language: AvailableLanguagesEnum, update: Update, context: CallbackContext) -> None:
    for i in range(random.randrange(2, 7)):
        timestamp = time.time()
        print(timestamp)
        push_to_github(timestamp, 'main', GITHUB_ACCESS_TOKEN)
