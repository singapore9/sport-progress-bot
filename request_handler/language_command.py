import requests

from messages import AvailableMessages, AvailableLanguagesEnum
from server_api import set_user_language
from .base import CommandHandler, URL


class LanguageCommandHandler(CommandHandler):
    @staticmethod
    def get_command_name():
        return "/language"

    def types_check(self, text_parts: list):
        msgs = []
        command, language = text_parts
        available_languages = {lang.name for lang in AvailableLanguagesEnum}
        if language not in available_languages:
            available_languages_str = ", ".join(sorted(available_languages))
            msgs.append(
                self.make_msg(
                    AvailableMessages.command__language__unknown_language,
                    [language, available_languages_str]
                )
            )
        return '\n'.join(msgs)

    def send_info_to_server(self, text_parts):
        command, language_name = text_parts
        r = set_user_language(self.user_id, AvailableLanguagesEnum[language_name])
        if r:
            self.post_msg(
                AvailableMessages.command__language__info_was_sent
            )

    def handle(self):
        text_parts = self.message_obj.message.text.split(' ')
        msg = ''
        if len(text_parts) != 2:
            msg = self.make_msg(
                AvailableMessages.command__language__arguments_error
            )
        else:
            checks_result = self.types_check(text_parts)
            if checks_result:
                pretext_msg = self.make_msg(
                    AvailableMessages.command__language__errors_pretext
                )
                msg = f"{pretext_msg}\n{checks_result}"
            else:
                self.send_info_to_server(text_parts)
                msg = self.make_msg(
                    AvailableMessages.command__language__info_was_saved
                )

        requests.post(URL, params={"chat_id": self.user_id, "text": msg})
