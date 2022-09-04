from typing import Type, List, Any

from enum import Enum, auto


class AvailableLanguagesEnum(Enum):
    eng = auto()
    bel = auto()


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
    def __init__(self, eng: str, bel: str):
        self.eng_template = eng
        self.bel_tamplate = bel

    def get(self, lang: AvailableLanguagesEnum):
        if lang == AvailableLanguagesEnum.eng:
            return self.eng_template
        elif lang == AvailableLanguagesEnum.bel:
            return self.bel_tamplate
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
    base_command__info_was_sent = auto()
    base_command__info_was_saved = auto()
    command__start = auto()
    command__activity_add__select = auto()
    command__activity_add__step1__select = auto()
    command__activity_add__step2__select = auto()
    command__activity_add__step3__select = auto()
    command__exercises = auto()
    command__language__select = auto()
    command__language__step1__select = auto()


MESSAGES = {
    AvailableMessages.base_command__info_was_sent: MessageWithParamsTemplate(
        eng="Sent:\n{}",
        bel="Адаслаў:\n{}"
    ),
    AvailableMessages.base_command__info_was_saved: MessageWithParamsTemplate(
        eng="Successfully saved:\n{}",
        bel="Паспехова захаваў:\n{}"
    ),
    AvailableMessages.command__start: MessageWithParamsTemplate(
        eng="Hi! I'm your progress saver. Share them with me.\nYour results will be here:\n{}",
        bel="Вітанкі! Буду тваім сябрам, занатоўваць твае поспехі.\nВось спасылка, па якой мажліва адсочваць іх:\n{}"
    ),
    AvailableMessages.command__activity_add__select: MessageTemplate(
        eng="Which kind of activity do you want to save:",
        bel="Вызнач, будзь ласка, якое практыкаванне жадаеш захаваць:"
    ),
    AvailableMessages.command__activity_add__step1__select: MessageTemplate(
        eng="Which kind of activity do you want to save:",
        bel="Вызнач, будзь ласка, якое практыкаванне жадаеш захаваць:"
    ),
    AvailableMessages.command__activity_add__step2__select: MessageWithParamsTemplate(
        eng="Please type repetitions count:\n{}",
        bel="Будзь ласка, вызнач колькасць разоў практыкавання:\n{}"
    ),
    AvailableMessages.command__activity_add__step3__select: MessageWithParamsTemplate(
        eng="Please type waiting time (seconds) before starting this set of repetitions:\n{}",
        bel="Колькі сякунд быў адпачынак да гэтага практыкавання?\n{}"
    ),
    AvailableMessages.command__exercises: MessageWithParamsTemplate(
        eng="I know about this list of activities:\n{}",
        bel="Я ведаю толькі гэтыя практыкаванні:\n{}"
    ),
    AvailableMessages.command__language__select: MessageTemplate(
        eng="Which language do you preffer?\nPlease, choose:",
        bel="Якую мову будзем выкарыстоўваць?\nВызнач, калі ласка:"
    ),
    AvailableMessages.command__language__step1__select: MessageTemplate(
        eng="Which language do you preffer?\nPlease, choose:",
        bel="Якую мову будзем выкарыстоўваць?\nВызнач, калі ласка:"
    ),
}


def make_msg(message_code: AvailableMessages, language: AvailableLanguagesEnum, params: List[Any] = None):
    message_template = MESSAGES[message_code]
    template_str = message_template.get(language)
    MessageClass = message_template.get_message_class()
    message = MessageClass(template_str, params)
    return message.compile()
