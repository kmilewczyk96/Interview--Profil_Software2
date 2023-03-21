import os
import datetime as dt
from unittest import TestCase
from mvc.model import Model


class TestModel(TestCase):
    def setUp(self) -> None:
        self.model = Model(court_number='TEST')

    def tearDown(self) -> None:
        if self.model.connection:
            self.model.connection.close()
        os.remove('tennis_court_TEST.db')

    def test_create_reservation_OK(self):
        """Tests if reservation is created given valid parameters."""
        res_start = dt.datetime.strptime('2025-01-01 15:00', '%Y-%m-%d %H:%M')
        res_end = dt.datetime.strptime('2025-01-01 16:00', '%Y-%m-%d %H:%M')
        self.model.create_reservation(
            name='John Doe',
            res_start=res_start,
            res_end=res_end
        )

        record = self.model.cursor.execute(
            "SELECT * FROM reservation"
        ).fetchone()
        self.assertIsNotNone(record)

    def test_delete_reservation_OK(self):
        """Tests if reservation is deleted when exists."""
        name = 'John Doe'
        res_start = dt.datetime.strptime('2025-01-01 19:00', '%Y-%m-%d %H:%M')
        res_end = dt.datetime.strptime('2025-01-01 20:30', '%Y-%m-%d %H:%M')
        self.model.create_reservation(
            name=name,
            res_start=res_start,
            res_end=res_end
        )

        self.model.delete_reservation(name=name, datetime_=res_start)
        record = self.model.cursor.execute(
            "SELECT * FROM reservation"
        ).fetchone()
        self.assertIsNone(record)

    def test_delete_reservation_FAIL(self):
        """Tests if error message is returned when trying to remove non-existing reservation."""
        name = 'John Doe'
        res_start = dt.datetime.strptime('2025-01-01 19:00', '%Y-%m-%d %H:%M')
        res_end = dt.datetime.strptime('2025-01-01 20:30', '%Y-%m-%d %H:%M')
        self.model.create_reservation(
            name=name,
            res_start=res_start,
            res_end=res_end
        )
        err, message = self.model.delete_reservation(name=name, datetime_=res_end)
        self.assertNotEqual(0, err)

    def test_get_schedule_data(self):
        """Tests if date dict is created and returned properly."""
        res_start_1 = dt.datetime.strptime('2025-01-01 19:00', '%Y-%m-%d %H:%M')
        res_end_1 = dt.datetime.strptime('2025-01-01 20:30', '%Y-%m-%d %H:%M')
        res_start_2 = dt.datetime.strptime('2025-01-02 19:00', '%Y-%m-%d %H:%M')
        res_end_2 = dt.datetime.strptime('2025-01-02 20:30', '%Y-%m-%d %H:%M')
        res_start_3 = dt.datetime.strptime('2025-01-05 19:00', '%Y-%m-%d %H:%M')
        res_end_3 = dt.datetime.strptime('2025-01-05 20:30', '%Y-%m-%d %H:%M')

        self.model.create_reservation(name='John Doe', res_start=res_start_1, res_end=res_end_1)
        self.model.create_reservation(name='Jane Doe', res_start=res_start_2, res_end=res_end_2)
        self.model.create_reservation(name='John D', res_start=res_start_3, res_end=res_end_3)

        dict_1 = len(self.model.get_schedule_data(date_from=res_start_1.date(), date_to=res_end_3.date()))
        dict_2 = len(self.model.get_schedule_data(date_from=res_start_1.date(), date_to=res_end_2.date()))
        dict_3 = len(self.model.get_schedule_data(date_from=res_start_1.date(), date_to=res_end_1.date()))

        self.assertEqual(dict_1, 5)
        self.assertEqual(dict_2, 2)
        self.assertEqual(dict_3, 1)

    def test_check_possible_reservations(self):
        """Tests if available reservation choices count is correct."""
        name = 'John Doe'
        res_start = dt.datetime.strptime('2025-01-01 19:00', '%Y-%m-%d %H:%M')
        res_end = dt.datetime.strptime('2025-01-01 20:30', '%Y-%m-%d %H:%M')
        self.model.create_reservation(
            name=name,
            res_start=res_start,
            res_end=res_end
        )

        possible_reservations_1 = len(self.model.check_possible_reservations(datetime_=dt.datetime.strptime(
            '2025-01-01 18:45', '%Y-%m-%d %H:%M'
        )))
        possible_reservations_2 = len(self.model.check_possible_reservations(datetime_=dt.datetime.strptime(
            '2025-01-01 18:30', '%Y-%m-%d %H:%M'
        )))
        possible_reservations_3 = len(self.model.check_possible_reservations(datetime_=dt.datetime.strptime(
            '2025-01-01 18:00', '%Y-%m-%d %H:%M'
        )))
        possible_reservations_4 = len(self.model.check_possible_reservations(datetime_=dt.datetime.strptime(
            '2025-01-01 15:00', '%Y-%m-%d %H:%M'
        )))

        self.assertEqual(possible_reservations_1, 0)
        self.assertEqual(possible_reservations_2, 1)
        self.assertEqual(possible_reservations_3, 2)
        self.assertEqual(possible_reservations_4, 3)
