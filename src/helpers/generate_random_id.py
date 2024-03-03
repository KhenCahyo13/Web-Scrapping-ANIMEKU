import random
import string

def generate_random_id(length = 16, prefix = ""):
    characters = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(characters) for i in range(length))
    random_id = prefix + random_part
    return random_id
