import re
from datetime import datetime as dt


class Validator:
    """Class containing various validators."""
    @staticmethod
    def validate_date(date_: str) -> bool:
        """Checks if provided date is valid. Returns True if it is, False otherwise."""
        # Double check because of the buggy behaviour of date format validation.
        if len(date_) != 10 or ' ' in date_:
            return False

        try:
            dt.strptime(date_, '%d.%m.%Y')
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def validate_date_range(date_from: str, date_to: str):
        date_from = dt.strptime(date_from, '%Y-%m-%d').date()
        date_to = dt.strptime(date_to, '%Y-%m-%d').date()

        if date_to < date_from:
            return False

        return True

    @staticmethod
    def validate_datetime(datetime_: str) -> bool:
        """Checks if provided datetime is valid. Returns True if it is, False otherwise."""
        # Double check because of the buggy behaviour of datetime format validation.
        if len(datetime_) != 16 or datetime_.count(' ') != 1:
            return False

        try:
            dt.strptime(datetime_, '%d.%m.%Y %H:%M')
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

    @staticmethod
    def validate_one_hour_limit(datetime_: str):
        datetime_ = dt.strptime(datetime_, '%Y-%m-%d %H:%M')
        now = dt.now()

        if (datetime_ - now).total_seconds() < 3600:
            return False

        return True
