from typing import List
from datetime import datetime
import psycopg2.extensions
from io import StringIO


class Employer:
    def __init__(self, full_name: str, birth_date: str, gender: str):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def save_to_bd(self, conn: psycopg2.extensions.connection) -> None:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO employees (full_name, birth_day, gender) VALUES (%s, %s, %s)',
                        (self.full_name, self.birth_date, self.gender))
        conn.commit()

    def get_how_old(self) -> int:
        birth_day = datetime.strptime(self.birth_date, '%Y-%m-%d')
        date_now = datetime.now()
        age = date_now.year - birth_day.year
        if date_now.month < birth_day.month or (date_now.month == birth_day.month and date_now.day < birth_day.day):
            age -= 1
        return age

    @classmethod
    def get_row(cls, row: tuple) -> "Employer":
        return cls(row[0], row[1], row[2])

    @staticmethod
    def data_array_save_to_db(conn: psycopg2.extensions.connection, employees: List['Employer']) -> None:
        f = StringIO()
        for employer in employees:
            f.write(f"{employer.full_name},{employer.birth_date},{employer.gender}\n")
        f.seek(0)
        with conn.cursor() as cursor:
            cursor.copy_from(f, "employees", sep=",", columns=("full_name", "birth_day", "gender"))
        conn.commit()
