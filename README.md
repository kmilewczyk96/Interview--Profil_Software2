># Tennis Court Reservation Manager:
>Author: Karol Milewczyk

>## Preparing dependencies:
>
>1) Install virtual environment in project's directory.
>2) With your venv activated, run `pip install -r requirements.txt`

>## How to run:
>> ### Main program:
>> With venv activated run `python main.py` command.
> 
>> ### Unit tests:
>> With venv activated run `python -m unittest` command.
 
>## How to use:
>>### User inputs:
>> 1) Choice: simply put corresponding index of the option that interests you.
>> 2) Datetime: enter date and hour that follows this pattern: {dd.mm.yyyy HH:MM}
>> 3) Date: enter date that follows this pattern: {dd.mm.yyyy}
>> 4) Filename: enter valid file name. Watch for restricted characters: \\, /, :, *, ?, ", <, >, and |.
>> 5) Name: simple string input.
>
>>### Program flow:
>> 1) Program starts from Main Menu and gives User choice to pick one of available options.
>> 2) Each choice got its own flow, after which User can get back to MainMenu or exit program.
>
>>### Main Menu options:
>> 1) Create a reservation allows User to create new reservation in the database.
>> 2) Delete a reservation allows User to delete reservation from the database.
>> 3) Print schedule allows User to print out all reservations from given date range.
>> 4) Save schedule to a file allows User to export all reservations from given date range to <br>
>> either csv or json file. Files will be saved into `exported_schedules` folder inside program's root folder.
>
>>### Exiting program:
>> You can either choose it from Main Menu, or if you are in the hurry use: `Ctrl + C` shortcut <br>
>> which will immediately quit program, catch KeyboardInterrupt error and clear your CLI screen.

> ## 3rd party libraries:
>> ### termcolor:
>> I used this library to add some style to the CLI. (colors and font weight)<br>
>> https://pypi.org/project/termcolor/
> 
>> ### python-dateutil
>> To avoid 'reinventing the wheel' I used one function from this module to get all dates from given range.<br>
>> https://pypi.org/project/python-dateutil/

> 
> ## Additional notes:
> 
> 1) By default, the CLI is cleared on some events, if you want to prevent this go to `mvc/view.py` <br> 
> and alter the `clear_screen` method.
> 2) Exporting schedules option does NOT prevent User from overwriting existing files with the same name.
