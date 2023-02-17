import datetime


#  регистрация новах пользователей в файл
def start_registration(message):
    make_start_time = datetime.datetime.now()
    make_start_time += datetime.timedelta(hours=3)  # Перевод в Московское время
    make_start_time = make_start_time.strftime('%d.%m.%Y-%H:%M')
    with open('data/mainFiles/list_registration.txt', 'a', encoding='utf-8') as f:
        print(message.from_user.id, make_start_time, sep=';', file=f)
