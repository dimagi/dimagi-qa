import random
import string

""""Genrates random strings that are passed as user inputs across various areasn in CCHQ"""

chars = string.ascii_lowercase + string.digits
random_string = ''.join(random.choices(chars, k=6))
N = 10
random_number = random.randint(100, 19999)


def fetch_random_string():
    return random_string


def fetch_phone_number():
    min_value = pow(10, N - 1)
    max_value = pow(10, N) - 1
    return str(random.randint(min_value, max_value))


def fetch_random_digit(start, end):
    return str(random.randint(start, end))
