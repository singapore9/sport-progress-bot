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
    command__exercises = auto()
    command__exercise_add__duplicate_error = auto()
    command__exercise_add__info_was_sent = auto()
    command__exercise_add__arguments_error = auto()
    command__exercise_add__errors_pretext = auto()
    command__exercise_add__info_was_saved = auto()


MESSAGES = {
    AvailableMessages.command__start: MessageTemplate(
        eng="Hi! I'm your progress saver. Share them with me.",
        bel="Вітанкі! Буду тваім сябрам, занатоўваць твае поспехі."
    ),
    AvailableMessages.unknown_command: MessageTemplate(
        eng="It is difficult for me to handle this info :(",
        bel="Пакуль што гэта незразумелая каманда для мяне :("
    ),
    AvailableMessages.command__activity_add__errors_pretext: MessageTemplate(
        eng="Too nice, but i don't understand...",
        bel="Цудоўна, але не ўсё зразумела..."
    ),
    AvailableMessages.command__activity_add__arguments_error: MessageTemplate(
        eng="Please, type `/activity_add activity_name iterations_count pause_before_item` and i will handle it :)",
        bel="Выкарыстоўвай, будзь ласка, такую форму "
            "`/activity_add назва_практыкавання колькасць_разоў адпачынак_перад_практыкаваннем` і я с задавальненнем "
            "запомню гэта :)"
    ),
    AvailableMessages.command__activity_add__unknown_activity: MessageWithParamsTemplate(
        eng="This '{}' activity is unknown. I can save info about this activities: {}.",
        bel="Гэтае практыкаванне '{}' невядома мне. Магу запомніць вось якія актыўнасці: {}."
    ),
    AvailableMessages.command__activity_add__iterations_count_error: MessageWithParamsTemplate(
        eng="You can't do 1.5 push-ups, so {} is incorrect number for counting activities in 1 iteration too.",
        bel="Як немагчыма выканаць 1.5 адціскванняў ад падлогі, "
            "так немагчыма выканаць і {} разоў ў адзінай ітэрацыі практыкавання."
    ),
    AvailableMessages.command__activity_add__pause_before_error: MessageWithParamsTemplate(
        eng="Relaxation can't be negative. {} is incorrect value.",
        bel="Нельга адпачыць меньш нуля хвілін/секунд. Таму {} - памылковая колькасць секунд."
    ),
    AvailableMessages.command__activity_add__info_was_sent: MessageTemplate(
        eng="Info about iteration was sent to our server.",
        bel="Адаслаў дадзенныя аб выкананам практыкаванні да серверу."
    ),
    AvailableMessages.command__activity_add__info_was_saved: MessageTemplate(
        eng="Info about iteration was saved. Thank you!",
        bel="Дадзенныя паспехова захваны. Дзякуй!"
    ),
    AvailableMessages.command__exercises: MessageWithParamsTemplate(
        eng="I know about this list of activities:\n{}",
        bel="Я ведаю толькі гэтыя практыкаванні:\n{}"
    ),
    AvailableMessages.command__exercise_add__duplicate_error: MessageWithParamsTemplate(
        eng="This exercise ({}) is already in list of allowed.",
        bel="Гэтае практыкаванне ({}) ужо вядома мне"
    ),
    AvailableMessages.command__exercise_add__errors_pretext: MessageTemplate(
        eng="I can't save info about this new type of activity because:",
        bel="Няма магчымасці захаваць новую назву практыкавання, таму што:"
    ),
    AvailableMessages.command__exercise_add__info_was_sent: MessageTemplate(
        eng="New exercise name was sent to our server.",
        bel="Я адаслаў назву новага практыкавання да серверу."
    ),
    AvailableMessages.command__exercise_add__info_was_saved: MessageTemplate(
        eng="New exercise was saved. Nice!",
        bel="Новае практыкаванне захавана. Цуд!"
    ),
    AvailableMessages.command__exercise_add__arguments_error: MessageTemplate(
        eng="Please, type `/exercise_add exercise_name` and i will handle it :)",
        bel="Прашу цябе, выкарыстоўвай форму `/exercise_add назва`. Вось тады я захаваю назву :)"
    )
}


def make_msg(message_code: AvailableMessages, language: AvailableLanguagesEnum, params: List[Any] = None):
    message_template = MESSAGES[message_code]
    template_str = message_template.get(language)
    MessageClass = message_template.get_message_class()
    message = MessageClass(template_str, params)
    return message.compile()
