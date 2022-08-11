from typing import Type, List, Any

from enum import Enum, auto


class AvailableLanguagesEnum(Enum):
    eng = auto()


class BaseMessage:
    def __init__(self, template: str, params: List[Any] = None):
        self.template = template
        self.params = params or []

    def compile(self) -> str:
        raise NotImplementedError


class Message(BaseMessage):
    def compile(self):
        return self.template


class MessageWithParams(BaseMessage):
    def __init__(self, template: str, params: List[Any]):
        super().__init__(template, params)

    def compile(self):
        return self.template.format(*self.params)


class BaseMessageTemplate:
    def __init__(self, eng: str):
        self.eng_template = eng

    def get(self, lang: AvailableLanguagesEnum):
        if lang == AvailableLanguagesEnum.eng:
            return self.eng_template
        return self.eng_template

    @classmethod
    def get_message_class(cls) -> Type[BaseMessage]:
        raise NotImplementedError


class MessageTemplate(BaseMessageTemplate):
    @classmethod
    def get_message_class(cls) -> Type[BaseMessage]:
        return Message


class MessageWithParamsTemplate(BaseMessageTemplate):
    @classmethod
    def get_message_class(cls) -> Type[BaseMessage]:
        return MessageWithParams


class AvailableMessages(Enum):
    command__start = auto()
    unknown_command = auto()
    command__activity_add = auto()
    command__activity_add__unknown_activity = auto()
    command__activity_add__errors_pretext = auto()
    command__activity_add__iterations_count_error = auto()
    command__activity_add__pause_before_error = auto()
    command__activity_add__info_was_sent = auto()
    command__activity_add__info_was_saved = auto()
    command__activity_add__arguments_error = auto()


MESSAGES = {
    AvailableMessages.command__start: MessageTemplate(
        eng="Hi! I'm your progress saver. Share them with me."
    ),
    AvailableMessages.unknown_command: MessageTemplate(
        eng="It is difficult for me to handle this info :("
    ),
    AvailableMessages.command__activity_add__errors_pretext: MessageTemplate(
        eng="Too nice, but i don't understand..."
    ),
    AvailableMessages.command__activity_add__arguments_error: MessageTemplate(
        eng="Please, type `/activity_add activity_name iterations_count pause_before_item` and i will handle it :)"
    ),
    AvailableMessages.command__activity_add__unknown_activity: MessageWithParamsTemplate(
        eng="This '{}' activity is unknown. I can save info about this activities: {}."
    ),
    AvailableMessages.command__activity_add__iterations_count_error: MessageWithParamsTemplate(
        eng="You can't do 1.5 push-ups, so {} is incorrect number for counting activities in 1 iteration too."
    ),
    AvailableMessages.command__activity_add__pause_before_error: MessageWithParamsTemplate(
        eng="Relaxation can't be negative. {} is incorrect value."
    ),
    AvailableMessages.command__activity_add__info_was_sent: MessageTemplate(
        eng="Info about iteration was saved. Thank you!"
    ),
    AvailableMessages.command__activity_add__info_was_saved: MessageTemplate(
        eng="Info about iteration was sent to out server."
    )
}


def make_msg(message_code: AvailableMessages, language: AvailableLanguagesEnum, params: List[Any] = None):
    message_template = MESSAGES[message_code]
    template_str = message_template.get(language)
    MessageClass = message_template.get_message_class()
    message = MessageClass(template_str, params)
    return message.compile()
