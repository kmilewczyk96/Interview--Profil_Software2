import csv
import datetime as dt
import json
import sqlite3

from dateutil import rrule


class Model:
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M'
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

    def create_reservation(self, name: str, datetime_: dt.datetime):
        datetime_ = datetime_.strftime(self.DATETIME_FORMAT)
        self.cursor.execute(f"INSERT INTO reservation VALUES ('{name}', '{datetime_}', '{datetime_}')")
        self.connection.commit()

    def delete_reservation(self, name: str, datetime_: dt.datetime) -> int:
        datetime_ = datetime_.strftime(self.DATETIME_FORMAT)
        time_to_delete = self.cursor.execute(
            f"SELECT * FROM reservation WHERE full_name='{name}' AND datetime_from='{datetime_}'"
        ).fetchone()
        if time_to_delete:
            self.cursor.execute(f"DELETE FROM reservation WHERE full_name='{name}' AND datetime_from='{datetime_}'")
            self.connection.commit()
            return self.OK
        else:
            return self.NO_RESERVATION_ERR

    def get_schedule_data(self, date_from: dt.date, date_to: dt.date) -> dict:
        # Creates dict for each day in provided range:
        dates_dict = {date_.date(): [] for date_ in rrule.rrule(
            freq=rrule.DAILY, dtstart=date_from, until=date_to
        )}

        date_from = date_from.strftime(self.DATE_FORMAT)
        date_to = date_to.strftime(self.DATE_FORMAT)

        schedule = self.cursor.execute(
            f"SELECT * FROM reservation "
            f"WHERE datetime_to > '{date_from}' AND datetime_from < '{date_to}'"
            f"ORDER BY datetime_from"
        ).fetchall()

        # Populates dates_dict with reservations:
        for name, res_start, res_end in schedule:
            date_ = dt.datetime.strptime(res_start, self.DATETIME_FORMAT).date()
            dates_dict[date_].append(
                (
                    name,
                    dt.datetime.strptime(res_start, self.DATETIME_FORMAT),
                    dt.datetime.strptime(res_end, self.DATETIME_FORMAT)
                )
            )

        return dates_dict

    def export_schedule_data(self, date_from: dt.date, date_to: dt.date, file_format: str, filename: str):
        dates_dict = self.get_schedule_data(date_from=date_from, date_to=date_to)

        match file_format:
            case 'csv':
                self._export_schedule_to_csv(data=dates_dict, filename=filename)
            case 'json':
                self._export_schedule_to_json(data=dates_dict, filename=filename)

    @staticmethod
    def _export_schedule_to_csv(data: dict, filename: str):
        with open(f'exported_schedules/{filename}.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['name', 'start', 'end'])
            for reservations in data.values():
                for name, start, end in reservations:
                    writer.writerow([
                        name,
                        start.strftime('%d.%m.%Y %H:%M'),
                        end.strftime('%d.%m.%Y %H:%M')
                    ])

    def _export_schedule_to_json(self, data: dict, filename: str):
        serialized_data = {}
        for date_, reservations in data.items():
            serialized_data[date_.strftime(self.DATE_FORMAT)] = self._serialize_reservations(reservations=reservations)

        with open(f'exported_schedules/{filename}.json', 'w') as json_file:
            json.dump(serialized_data, json_file)

    def _prepare_db(self):
        try:
            self.cursor.execute('CREATE TABLE reservation(full_name varchar, datetime_from time, datetime_to time)')
        except sqlite3.OperationalError:
            pass

    @staticmethod
    def _serialize_reservations(reservations: list):
        serialized_reservations = []
        for reservation in reservations:
            name, date_from, date_to = reservation
            time_from = date_from.time().strftime('%H:%M')
            time_to = date_to.time().strftime('%H:%M')
            serialized_reservations.append(
                {
                    "name": name,
                    "start_time": time_from,
                    "end_time": time_to
                }
            )

        return serialized_reservations
