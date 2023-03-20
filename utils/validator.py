import re
import datetime as dt


class Validator:
    """Class containing various validators."""
    @staticmethod
    def validate_date_range(date_from: dt.date, date_to: dt.date):
        if date_from > date_to:
            return False

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
    def validate_one_hour_limit(datetime_: dt.datetime):
        if (datetime_ - dt.datetime.now()).total_seconds() < 3600:
            return False

        return True

    @staticmethod
    def validate_is_in_future(datetime_: dt.datetime):
        if (datetime_ - dt.datetime.now()).total_seconds() < 0:
            return False

        return True