import yadisk
from data import YA_TOKEN, root_src
import random

y = yadisk.YaDisk(token=YA_TOKEN)

# Проверяет, валиден ли токен
print(y.check_token())

# Получает общую информацию о диске
print(y.get_disk_info())


def load_to_disk(src, floor, room):
    with open(src, "rb") as f:
        y.upload(f, f"{root_src}/{floor}/{room}/{random.randrange(1000)}.jpg")
