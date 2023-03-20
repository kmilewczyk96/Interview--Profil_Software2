from unittest import TestCase

from utils.validator import Validator


class TestValidator(TestCase):
    """Tests Validator methods."""
    validator = Validator()

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
