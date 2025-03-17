import logging
import time
from typing import Optional
from database import get_connection
from models import Employer
from utils import generate_random_employee

logging.basicConfig(level=logging.INFO)


def mode_1() -> None:
    create_table = """
    CREATE TABLE IF NOT EXISTS employees(
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    birth_day Varchar(10) NOT NULL,
    gender Varchar(20) NOT NULL)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(create_table)
            conn.commit()
    logging.info('Таблица создана')


def mode_2(full_name: str, birth_date: str, gender: str) -> None:
    create_employer = Employer(full_name, birth_date, gender)
    with get_connection() as conn:
        create_employer.save_to_bd(conn)
    logging.info(f'Добавили сотрудника {create_employer.full_name}. Полных лет: {create_employer.get_how_old()}.')


def mode_3() -> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT DISTINCT full_name, birth_day, gender
            FROM employees
            ORDER BY full_name, birth_day;
            """)
            result = cursor.fetchall()
            for row in result:
                row_employer = Employer.get_row(row)
                print(f'Полное имя: {row_employer.full_name}, '
                      f'Дата рождения: {row_employer.birth_date}, '
                      f'Пол: {row_employer.gender}, '
                      f'Полных лет: {row_employer.get_how_old()}')


def mode_4(start_letter_for_filter: Optional[str] = None, gender: str = 'Male') -> None:
    start_time = time.time()
    total_records = 1_000_000
    task_records = 100
    package_size = 10_000

    with get_connection() as conn:
        for i in range(0, total_records - task_records, package_size):
            package = [generate_random_employee() for _ in
                       range(min(package_size, total_records - task_records - i))]
            Employer.data_array_save_to_db(conn, package)
        batch = [generate_random_employee(start_letter_for_filter) for _ in range(task_records)]
        for emp in batch:
            emp.gender = gender
        Employer.data_array_save_to_db(conn, batch)

    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f'Добавлено {total_records} записей. Общее время выполнения: {total_time:.2f} секунд')


def mode_5() -> float:
    start_time = time.time()
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT full_name, birth_day, gender "
                           "FROM employees "
                           "WHERE full_name LIKE 'F%' AND gender = 'Male'")
            result = cursor.fetchall()
            for row in result:
                employer = Employer.get_row(row)
                print(employer.full_name, employer.gender)
    end_time = time.time()
    time_spent = (end_time - start_time)
    logging.info(f'заняло времени {time_spent:.2f}')
    return time_spent


def mode_6() -> None:
    time_before = mode_5()
    logging.info(f"До оптимизации: {time_before:.3f} секунд")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""DROP INDEX IF EXISTS index_for_table ;""")
            cursor.execute(
                """
                CREATE INDEX index_for_table  
                ON employees (full_name text_pattern_ops, gender);
                """
            )
            cursor.execute("""ANALYZE employees;""")
        conn.commit()

    print("\nПосле оптимизации (добавлен индекс на full_name):")
    time_after = mode_5()
    print("\nРезультаты оптимизации:")
    print(f"Время до оптимизации: {time_before:.3f} секунд")
    print(f"Время после оптимизации: {time_after:.3f} секунд")
    print(f"Ускорение: {time_before - time_after:.3f} секунд")
    print(
        "Индекс на full_name ускоряет фильтрацию WHERE gender = 'Male' и full_name LIKE 'F%'."
    )
