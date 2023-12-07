import random


def generate_otp():
    otp = str(random.randint(1000, 9999))
    return otp
