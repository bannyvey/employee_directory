from typing import Optional
from faker import Faker
import random
from models import Employer

fake = Faker("en_US")


def generate_random_employee(start_letter: Optional[str] = None) -> Employer:
    if start_letter:
        while True:
            last_name = fake.last_name()
            if last_name.startswith(start_letter.upper()):
                break
    else:
        last_name = fake.last_name()

    first_name = fake.first_name()
    full_name = f"{last_name} {first_name}"
    birth_day = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d")
    gender = random.choice(["Male", "Female"])
    return Employer(full_name, birth_day, gender)
