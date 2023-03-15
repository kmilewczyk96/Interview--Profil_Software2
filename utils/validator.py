import re
from datetime import datetime as dt


class Validator:
    """Class containing various validators."""
    @staticmethod
    def validate_choice(choice: str, choices: tuple) -> bool:
        """Checks if provided choice is withing choices range. Returns True if it is, False otherwise."""
        if choice in choices:
            return True

        return False

    @staticmethod
    def validate_date(date: str) -> bool:
        """Checks if provided date is valid. Returns True if it is, False otherwise."""
        # Double check because of the buggy behaviour of datetime format validation.
        if len(date) != 16 or date.count(' ') != 1:
            return False

        try:
            dt.strptime(date, '%d.%m.%Y %H:%M')
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def validate_filename(filename: str) -> bool:
        """Checks if provided filename doesn't contain restricted characters.
        Returns True if it is valid, False otherwise."""
        is_empty = len(filename.strip()) == 0
        invalid_signs = re.search(r'[\\/:*?"<>|]+', filename)

        if not is_empty and not invalid_signs:
            return True

        return False
