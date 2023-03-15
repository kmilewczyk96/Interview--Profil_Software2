from unittest import TestCase

from utils.validator import Validator


class TestValidator(TestCase):
    """Tests Validator methods."""
    validator = Validator()

    def test_validate_choice_valid(self):
        """Tests if choices are validated correctly when valid."""
        choice = '1'
        choices = ('1', '2')

        self.assertTrue(self.validator.validate_choice(choice=choice, choices=choices))

    def test_validate_choice_invalid(self):
        """Tests if choices are validated correctly when invalid."""
        choice_1 = ''
        choices_1 = ('1', '2')
        choice_2 = '1 '
        choices_2 = ('1', '2')

        self.assertFalse(self.validator.validate_choice(choice=choice_1, choices=choices_1))
        self.assertFalse(self.validator.validate_choice(choice=choice_2, choices=choices_2))

    def test_validate_date_valid(self):
        """Tests if dates are validated correctly when valid."""
        date_1 = '12.12.1995 09:15'
        date_2 = '01.06.2020 13:15'
        date_3 = '10.03.2025 23:59'
        date_4 = '29.02.2024 13:13'
        date_5 = '10.03.2025 00:00'

        self.assertTrue(self.validator.validate_date(date=date_1))
        self.assertTrue(self.validator.validate_date(date=date_2))
        self.assertTrue(self.validator.validate_date(date=date_3))
        self.assertTrue(self.validator.validate_date(date=date_4))
        self.assertTrue(self.validator.validate_date(date=date_5))

    def test_validate_date_invalid(self):
        """Tests if dates are validated correctly when invalid."""
        date_1 = '01.12.2021  9:15'
        date_2 = '1.12.2021 09:15'
        date_3 = '01.12.2025 09:155'
        date_4 = '29.02.2023 09:15'
        date_5 = '12.05.2022 24:00'

        self.assertFalse(self.validator.validate_date(date=date_1))
        self.assertFalse(self.validator.validate_date(date=date_2))
        self.assertFalse(self.validator.validate_date(date=date_3))
        self.assertFalse(self.validator.validate_date(date=date_4))
        self.assertFalse(self.validator.validate_date(date=date_5))

    def test_validate_filename_valid(self):
        """Tests if filenames are validated correctly when valid."""
        filename_1 = 'filename'
        filename_2 = 'dot.before.extension'
        filename_3 = 'snake_case'
        filename_4 = '1234567890'
        filename_5 = '[some][signs][allowed]'

        self.assertTrue(self.validator.validate_filename(filename_1))
        self.assertTrue(self.validator.validate_filename(filename_2))
        self.assertTrue(self.validator.validate_filename(filename_3))
        self.assertTrue(self.validator.validate_filename(filename_4))
        self.assertTrue(self.validator.validate_filename(filename_5))

    def test_validate_filename_invalid(self):
        """Tests if filenames are validated correctly when invalid."""
        filename_1 = ' '
        filename_2 = 'filename\\'
        filename_3 = 'name?'
        filename_4 = 'Not|Allowed'
        filename_5 = '[some][signs]<not>'

        self.assertFalse(self.validator.validate_filename(filename_1))
        self.assertFalse(self.validator.validate_filename(filename_2))
        self.assertFalse(self.validator.validate_filename(filename_3))
        self.assertFalse(self.validator.validate_filename(filename_4))
        self.assertFalse(self.validator.validate_filename(filename_5))
