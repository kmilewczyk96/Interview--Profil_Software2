import csv
import datetime as dt
import json
import os.path
import sqlite3

from dateutil import rrule


class Model:
    DB_DATE_FORMAT = '%Y-%m-%d'
    DB_DATETIME_FORMAT = '%Y-%m-%d %H:%M'
    CSV_DATETIME_FORMAT = '%d.%m.%Y %H:%M'
    JSON_DATE_FORMAT = '%d.%m.%Y'
    JSON_HOUR_FORMAT = '%H:%M'

    OK, ERROR = range(2)

    def __init__(self, court_number=1):
        self.connection = sqlite3.connect(f'tennis_court_{court_number}.db')
        self.cursor = self.connection.cursor()
        self._prepare_db()

    def create_reservation(self, name: str, res_start: dt.datetime, res_end: dt.datetime):
        res_start = res_start.strftime(self.DB_DATETIME_FORMAT)
        res_end = res_end.strftime(self.DB_DATETIME_FORMAT)
        self.cursor.execute(f"INSERT INTO reservation VALUES ('{name}', '{res_start}', '{res_end}')")
        self.connection.commit()

    def delete_reservation(self, name: str, datetime_: dt.datetime) -> tuple:
        datetime_ = datetime_.strftime(self.DB_DATETIME_FORMAT)
        time_to_delete = self.cursor.execute(
            f"SELECT * FROM reservation WHERE full_name='{name}' AND datetime_from='{datetime_}'"
        ).fetchone()
        if time_to_delete:
            self.cursor.execute(f"DELETE FROM reservation WHERE full_name='{name}' AND datetime_from='{datetime_}'")
            self.connection.commit()
            return self.OK, 'Your reservation has been canceled successfully.'
        else:
            return self.ERROR, 'Reservation does not exist!'

    def get_schedule_data(self, date_from: dt.date, date_to: dt.date) -> dict:
        # Creates dict for each day in provided range:
        dates_dict = {date_.date(): [] for date_ in rrule.rrule(
            freq=rrule.DAILY, dtstart=date_from, until=date_to
        )}

        schedule = self.cursor.execute(
            f"SELECT * FROM reservation "
            f"WHERE datetime_to > '{date_from}' AND datetime_from < '{date_to}'"
            f"ORDER BY datetime_from"
        ).fetchall()

        # Populates dates_dict with reservations:
        for name, res_start, res_end in schedule:
            date_ = dt.datetime.strptime(res_start, self.DB_DATETIME_FORMAT).date()
            dates_dict[date_].append(
                (
                    name,
                    dt.datetime.strptime(res_start, self.DB_DATETIME_FORMAT),
                    dt.datetime.strptime(res_end, self.DB_DATETIME_FORMAT)
                )
            )

        return dates_dict

    def export_schedule_data(self, date_from: dt.date, date_to: dt.date, file_format: str, filename: str):
        dates_dict = self.get_schedule_data(date_from=date_from, date_to=date_to)
        exports_directory = 'exported_schedules'
        filename = os.path.join(exports_directory, filename)
        abs_path = os.path.abspath(filename)

        match file_format:
            case 'csv':
                self._export_schedule_to_csv(data=dates_dict, filename=filename)
                return self.OK, f'Successfully created: {abs_path}.csv.'
            case 'json':
                self._export_schedule_to_json(data=dates_dict, filename=filename)
                return self.OK, f'Successfully created: {abs_path}.json.'

    def check_possible_reservations(self, datetime_: dt.datetime) -> list:
        reservation_length_choices = []
        colliding_reservation = self.cursor.execute(
            f"SELECT * FROM reservation "
            f"WHERE datetime_from <= '{datetime_}' AND datetime_to > '{datetime_}'"
        ).fetchone()

        if colliding_reservation:
            return reservation_length_choices

        for interval_multipliers in range(1, 4):
            datetime_ += dt.timedelta(seconds=1800)
            colliding_reservation = self.cursor.execute(
                f"SELECT * FROM reservation "
                f"WHERE datetime_from < '{datetime_.strftime(self.DB_DATETIME_FORMAT)}' "
                f"AND datetime_to > '{datetime_.strftime(self.DB_DATETIME_FORMAT)}'"
            ).fetchone()
            if colliding_reservation:
                break

            reservation_length_choices.append(interval_multipliers * 30)

        return reservation_length_choices

    def _export_schedule_to_csv(self, data: dict, filename: str):
        with open(f'{filename}.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['name', 'start', 'end'])
            for reservations in data.values():
                for name, start, end in reservations:
                    writer.writerow([
                        name,
                        start.strftime(self.CSV_DATETIME_FORMAT),
                        end.strftime(self.CSV_DATETIME_FORMAT)
                    ])

    def _export_schedule_to_json(self, data: dict, filename: str):
        serialized_data = {}
        for date_, reservations in data.items():
            serialized_data[date_.strftime(self.JSON_DATE_FORMAT)] = \
                self._serialize_reservations(reservations=reservations)

        with open(f'{filename}.json', 'w') as json_file:
            json.dump(serialized_data, json_file)

    def _prepare_db(self):
        try:
            self.cursor.execute('CREATE TABLE reservation(full_name varchar, datetime_from time, datetime_to time)')
        except sqlite3.OperationalError:
            pass

    def _serialize_reservations(self, reservations: list):
        serialized_reservations = []
        for reservation in reservations:
            name, date_from, date_to = reservation
            time_from = date_from.time().strftime(self.JSON_HOUR_FORMAT)
            time_to = date_to.time().strftime(self.JSON_HOUR_FORMAT)
            serialized_reservations.append(
                {
                    "name": name,
                    "start_time": time_from,
                    "end_time": time_to
                }
            )

        return serialized_reservations

    def check_if_eligible(self, name: str, datetime_: dt.datetime):
        weekday = datetime_.weekday()
        date_ = datetime_.date()
        week_start = date_ - dt.timedelta(days=weekday)
        week_end = date_ + dt.timedelta(days=6 - weekday)

        user_reservation_count = len(
            self.cursor.execute(
                f"SELECT * FROM reservation "
                f"WHERE full_name='{name}' "
                f"AND datetime_from >= '{week_start}' AND datetime_from <= '{week_end}'"
            ).fetchall()
        )

        if user_reservation_count > 2:
            print('not eligible')
        else:
            print('eligible')

    def recommend_other_date(self, datetime_: dt.datetime):
        reservations = self.cursor.execute(
            f"SELECT * FROM reservation "
            f"WHERE datetime_to > '{datetime_}'"
            f"ORDER BY datetime_from"
        ).fetchall()
        print(reservations)

        for i, reservation in enumerate(reservations[:-1]):
            current_end = dt.datetime.strptime(reservation[2], self.DB_DATETIME_FORMAT)
            next_start = dt.datetime.strptime(reservations[i + 1][1], self.DB_DATETIME_FORMAT)

            delta = (next_start - current_end).total_seconds()
            if delta >= 1800:
                return current_end

        # If no space in-between existing reservations, return end of last reservation.
        return dt.datetime.strptime(reservations[-1][2], self.DB_DATETIME_FORMAT)
