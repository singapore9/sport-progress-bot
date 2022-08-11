from fastapi import FastAPI

from model import UserMessage
from request_handler import HANDLED_COMMANDS, UnknownTextHandler

app = FastAPI()


@app.get("/")
async def read_route():
    return "CHAT-BOT IS UP :)"


@app.post("/")
def chatbot(received_msg: UserMessage):
    splitted_text = received_msg.message.text.split(' ')
    probably_command = splitted_text and splitted_text[0]

    HandlerClass = UnknownTextHandler
    for handler_class in HANDLED_COMMANDS:
        if handler_class.get_command_name() == probably_command:
            HandlerClass = handler_class
            break

    handler = HandlerClass(received_msg)
    handler.handle()
