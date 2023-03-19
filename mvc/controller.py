import sys
import datetime as dt

from mvc.model import Model
from mvc.view import View


class Controller:
    DATE_FORMAT = '%d.%m.%Y'
    DATETIME_FORMAT = '%d.%m.%Y %H:%M'

    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.initial_launch = True

    def start(self):
        self.view.clear_screen()

        if self.initial_launch:
            self.view.print_header(header='Welcome to Tennis Court REPL.')
            self.initial_launch = False
        else:
            self.view.print_header(header='Main Menu.')

        main_menu_choices = (
            'Make a reservation',
            'Cancel a reservation',
            'Print schedule.',
            'Save schedule to a file.',
            'Exit.'
        )
        choice = self._prompt_choice(question='Please choose one of the available options.', choices=main_menu_choices)
        self.view.print_header(header=main_menu_choices[choice])
        match choice:
            case 0:
                self._create_reservation()
            case 1:
                self._delete_reservation()
            case 2:
                self._print_schedule()
            case 3:
                self._export_to_file()
            case 4:
                self._exit_program()

        self._continue_work()

    # Main Menu flows:
    def _create_reservation(self):
        self.view.print_question(question='When would you like to make reservation? (dd.mm.yyyy HH:MM)')
        datetime_ = self._prompt_datetime()
        self.view.print_question(question='What is your name?')
        name = self._prompt_name()
        self.model.create_reservation(datetime_=datetime_, name=name)

    def _delete_reservation(self) -> None:
        self.view.print_question(question='What is your name?')
        name = self._prompt_name()
        self.view.print_question(question='What is the date of your reservation?')
        datetime_ = self._prompt_datetime()

        err_code = self.model.delete_reservation(name=name, datetime_=datetime_)
        if err_code:
            self.view.print_error(error_message=self.model.ERRORS[err_code])
        else:
            self.view.print_success(success_message='Your reservation has been canceled successfully.')

    def _print_schedule(self):
        self.view.print_question(question='Date (from): (dd.mm.yyyy)')
        date_from = self._prompt_date()
        self.view.print_question(question='Date (to): (dd.mm.yyyy)')
        date_to = self._prompt_date()

        schedule_data = self.model.get_schedule_data(date_from=date_from, date_to=date_to)
        self.view.print_schedule(schedule_data=schedule_data)

    def _export_to_file(self):
        self.view.print_question(question='Date (from): (dd.mm.yyyy)')
        date_from = self._prompt_date()
        self.view.print_question(question='Date (to): (dd.mm.yyyy)')
        date_to = self._prompt_date()

        format_choices = (
            'csv',
            'json'
        )
        choice = self._prompt_choice(
            question='Please pick desired file format:',
            choices=format_choices
        )
        file_format = format_choices[choice]

        self.view.print_question(question='Please provide desired filename')
        filename = self._prompt_filename()

        self.model.export_schedule_data(
            date_from=date_from,
            date_to=date_to,
            file_format=file_format,
            filename=filename
        )

    def _exit_program(self):
        confirmation_choices = (
            'Yes',
            'No'
        )
        choice = self._prompt_choice(question='Are you sure?', choices=confirmation_choices)
        match choice:
            case 0:
                self.view.clear_screen()
                sys.exit()
            case 1:
                self.start()

    def _continue_work(self):
        confirmation_choices = (
            'Yes, continue.',
            'No, exit program.'
        )
        choice = self._prompt_choice(question='Do you want to do anything else?', choices=confirmation_choices)
        match choice:
            case 0:
                self.start()
            case 1:
                self.view.clear_screen()
                sys.exit()

    # Prompts:
    def _prompt_choice(self, question: str, choices: tuple) -> int:
        self.view.print_question(question=question)
        self.view.print_ordered_list(choices=choices)

        while True:
            pick = self._pretty_input()
            try:
                pick = int(pick) - 1
                _ = choices[pick]
            except (ValueError, IndexError):
                self.view.print_error('Please provide valid option.')
            else:
                return pick

    def _prompt_date(self) -> dt.date:
        while True:
            date_ = self._pretty_input()
            try:
                date_ = dt.datetime.strptime(date_, self.DATE_FORMAT).date()
            except ValueError:
                self.view.print_error('Please provide a valid date.')
            else:
                return date_

    def _prompt_datetime(self) -> dt.datetime:
        while True:
            datetime_ = self._pretty_input()
            try:
                datetime_ = dt.datetime.strptime(datetime_, self.DATETIME_FORMAT)
            except ValueError:
                self.view.print_error('Please provide a valid date.')
            else:
                return datetime_

    def _prompt_filename(self):
        while True:
            filename = self._pretty_input()
            return filename

    def _prompt_name(self):
        while True:
            name = self._pretty_input()
            if len(name.strip()) != 0:
                return name
            else:
                self.view.print_error('Please provide non-empty name.')

    # Utils:
    def _pretty_input(self):
        try:
            input_ = input('>'.ljust(self.view.tab_length))
        except KeyboardInterrupt:
            self.view.clear_screen()
            sys.exit()
        else:
            return input_
