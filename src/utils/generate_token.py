import random


def generate_verify_token():
    token = random.randint(100000, 999999)
    return token
