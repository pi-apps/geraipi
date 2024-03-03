import random
import string


def get_random(lengttext=5):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=lengttext))
