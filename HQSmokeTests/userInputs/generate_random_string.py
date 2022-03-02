import random
import string

chars = string.ascii_lowercase + string.digits
random_string = ''.join(random.choices(chars, k=6))
N = 10

def fetch_random_string():
    return random_string

def fetch_phone_number():
    min = pow(10, N - 1)
    max = pow(10, N) - 1
    return str(random.randint(min, max))
