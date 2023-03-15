from tennis_court import TennisCourt
from utils.aesthetic_print import aesthetic_print


def run():
    model = TennisCourt()
    print(aesthetic_print(text='Welcome to Tennis Court REPL.'))

    while True:
        x = input(
            'Please choose one of available options listed below:\n'
            ' 1. Make a reservation.\n'
            ' 2. Cancel a reservation.\n'
            ' 3. Print schedule.\n'
            ' 4. Save schedule to a file.\n'
            ' 5. Exit.\n'
            '> '
        )
        match x:
            case '1':
                print(aesthetic_print(text='CREATE RESERVATION'))
                name = input(
                    'What\'s your name?\n'
                    '> '
                )
                date = input(
                    'When would you like to book? {DD:MM:YYYY HH:MM}\n'
                    '> '
                )
                print(model.create_reservation(name=name, date=date))

            case '2':
                print(aesthetic_print(text='CANCEL RESERVATION'))
                name = input(
                    'What\'s your name?\n'
                    '> '
                )
                date = input(
                    'When would you like to book? {DD:MM:YYYY HH:MM}\n'
                    '> '
                )
                print(model.cancel_reservation(name=name, date=date))

            case '3':
                date_from = input(
                    'Date from:\n'
                    '> '
                )
                date_to = input(
                    'Date to:\n'
                    '> '
                )
                print(model.print_schedule(date_from, date_to))

            case '4':
                date_from = input(
                    'Date from:\n'
                    '> '
                )
                date_to = input(
                    'Date to:\n'
                    '> '
                )
                file_format = input(
                    'Please pick from options below:\n'
                    '1. csv\n'
                    '2. json\n'
                    '> '
                )
                filename = input(
                    'Please provide a filename.\n'
                    '> '
                )
                print(model.export_schedule(
                    date_from=date_from,
                    date_to=date_to,
                    data_format=file_format,
                    filename=filename
                ))

            case '5':
                print(aesthetic_print(text='GOODBYE!'))
                exit()

            case _:
                print('Fail')


if __name__ == '__main__':
    run()