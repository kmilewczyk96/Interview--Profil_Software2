import sqlite3
from datetime import datetime as dt
from dateutil import rrule


class Model:
    (
        OK,
        NO_RESERVATION_ERR
    ) = range(2)
    ERRORS = {
        NO_RESERVATION_ERR: 'Reservation does not exist!'
    }

    def __init__(self, court_number=1):
        self.connection = sqlite3.connect(f'tennis_court_{court_number}.db')
        self.cursor = self.connection.cursor()
        self._prepare_db()

    def create_reservation(self, name: str, datetime_: str):
        self.cursor.execute(f"INSERT INTO reservation VALUES ('{name}', '{datetime_}', '{datetime_}')")
        self.connection.commit()

    def delete_reservation(self, name: str, datetime_: str):
        time_to_delete = self.cursor.execute(
            f"SELECT * FROM reservation WHERE full_name='{name}' AND datetime_from='{datetime_}'"
        ).fetchone()
        if time_to_delete:
            self.cursor.execute(f"DELETE FROM reservation WHERE full_name='{name}' AND datetime_from='{datetime_}'")
            self.connection.commit()
            return self.OK
        else:
            return self.NO_RESERVATION_ERR

    def get_schedule_data(self, date_from: str, date_to: str):
        schedule = self.cursor.execute(
            f"SELECT * FROM reservation "
            f"WHERE datetime_to > '{date_from}' AND datetime_from < '{date_to}'"
            f"ORDER BY datetime_from"
        ).fetchall()

        date_from = dt.strptime(date_from, '%Y-%m-%d')
        date_to = dt.strptime(date_to, '%Y-%m-%d')

        # Creates dict for each day in provided range:
        dates_dict = {date_.strftime('%Y-%m-%d'): [] for date_ in rrule.rrule(
            freq=rrule.DAILY, dtstart=date_from, until=date_to
        )}
        # Populates above dict with reservations data:
        for name, res_start, res_end in schedule:
            res_start_date = dt.strptime(res_start, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d')
            dates_dict[res_start_date].append((name, res_start, res_end))

        return dates_dict

    def export_schedule_data(self, date_from: str, date_to: str, data_format: str, filename: str):
        schedule = self.cursor.execute(
            f"SELECT * FROM reservation "
            f"WHERE datetime_to > '{date_from}' AND datetime_from < '{date_to}'"
            f"ORDER BY datetime_from"
        ).fetchall()

    def _prepare_db(self):
        try:
            self.cursor.execute('CREATE TABLE reservation(full_name varchar, datetime_from time, datetime_to time)')
        except sqlite3.OperationalError:
            pass
