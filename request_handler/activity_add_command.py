import requests

from messages import AvailableMessages
from server_api import send_activity, get_exercises
from .base import CommandHandler, URL


class ActivityAddCommandHandler(CommandHandler):
    @staticmethod
    def get_command_name():
        return "/activity_add"

    def types_check(self, text_parts: list):
        msgs = []
        command, activity_name, iterations_count, pause_before_item = text_parts
        allowed_activities = get_exercises()
        if activity_name not in allowed_activities:
            activities_str = ", ".join(allowed_activities)
            msgs.append(
                self.make_msg(
                    AvailableMessages.command__activity_add__unknown_activity,
                    [activity_name, activities_str]
                )
            )
        try:
            int(iterations_count)
            if int(iterations_count) < 1:
                raise ValueError
        except ValueError:
            msgs.append(
                self.make_msg(
                    AvailableMessages.command__activity_add__iterations_count_error,
                    [iterations_count]
                )
            )
        try:
            float(pause_before_item)
            if float(pause_before_item) < 0:
                raise ValueError
        except ValueError:
            msgs.append(
                self.make_msg(
                    AvailableMessages.command__activity_add__pause_before_error,
                    [pause_before_item]
                )
            )
        return '\n'.join(msgs)

    def send_info_to_server(self, text_parts):
        command, activity_name, iterations_count, pause_before_item = text_parts
        iterations_count = int(iterations_count)
        pause_before_item = float(pause_before_item)
        r = send_activity(activity_name, iterations_count, pause_before_item)
        if r:
            self.post_msg(
                AvailableMessages.command__activity_add__info_was_sent
            )

    def handle(self):
        text_parts = self.message_obj.message.text.split(' ')
        msg = ''
        if len(text_parts) != 4:
            msg = self.make_msg(
                AvailableMessages.command__activity_add__arguments_error
            )
        else:
            checks_result = self.types_check(text_parts)
            if checks_result:
                pretext_msg = self.make_msg(
                    AvailableMessages.command__activity_add__errors_pretext
                )
                msg = f"{pretext_msg}\n{checks_result}"
            else:
                self.send_info_to_server(text_parts)
                msg = self.make_msg(
                    AvailableMessages.command__activity_add__info_was_saved
                )

        requests.post(URL, params={"chat_id": self.user_id, "text": msg})
