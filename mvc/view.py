import os
import datetime as dt
from termcolor import cprint


class View:
    DATE_FORMAT = '%d.%m.%Y'
    DATETIME_FORMAT = '%d.%m.%Y %H:%M'

    def __init__(self, separator_sign='=', width=50, tab_length=2):
        self.separator = separator_sign * width
        self.width = width
        self.tab_length = tab_length
        self.tab = ' ' * tab_length

    @staticmethod
    def clear_screen() -> None:
        """Clears the CLI screen."""
        os_name = os.name

        if os_name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def print_error(self, error_message: str) -> None:
        """Prints provided error message with some styling."""
        error_message = self.tab + error_message
        cprint(text=error_message, color='red')

    def print_header(self, header: str) -> None:
        """Prints provided header text, with some styling."""
        print(self.separator)
        cprint(text=header.center(self.width), attrs=['bold'])
        print(self.separator)

    def print_ordered_list(self, choices: tuple) -> None:
        for pos, choice in enumerate(choices):
            print(f'{self.tab}{pos + 1}. {choice}')

    def print_schedule(self, schedule_data: dict):
        for day, reservations in schedule_data.items():
            print(self.tab + self._pretty_date(date_=day))
            if reservations:
                for reservation in reservations:
                    name, res_start, res_end = reservation
                    print(f'{self.tab * 2}{name}: {res_start} - {res_end}')
            else:
                print(self.tab * 2 + 'No reservations.')
            print('')

    def print_success(self, success_message: str) -> None:
        """Prints provided success message with some styling."""
        success_message = self.tab + success_message
        cprint(text=success_message, color='green')

    def print_question(self, question: str) -> None:
        question = self.tab + question
        print(question)

    # Utils:
    def _pretty_date(self, date_: dt.date) -> str:
        today = dt.date.today()
        day_delta = (date_ - today).days

        if day_delta == 0:
            return 'Today'
        if day_delta < 0:
            return f"{date_.strftime(self.DATE_FORMAT)} (Archive)"
        if day_delta == 1:
            return 'Tomorrow'
        if day_delta <= 6:
            return date_.strftime('%A')
        if date_.year == today.year:
            return date_.strftime('%d.%m')

        return date_.strftime(self.DATE_FORMAT)
