- настроить nginx
- настроить ci/cd (travis ci (linter + tests) + heroku yml)
  задеплоить куда-нибудь

- покрыть тестами (TDD)

- нужны пользователи, чтобы могли авторизовываться через basic auth
  создать пользователя revolut
  дать интерфейс drf, чтобы могли потестить апи из браузера


# TODO
пустой массив
передается на вход не массив
не json serializable
массив, состоящий из словарей разных структур

передать json_array не плоский

передать параметров больше, чем количество ключей
передать несуществующий ключ отдельно и в цепочке

обратить внимание на алгоритмическую сложность и используемую память

использовать какой-нибудь паттерн
не использовать сторонние библиотеки, была бы возможность вынести этот скрипт и все будет работать

[
['USD', 'US', 'Boston', 100],
['EUR', 'FR', 'Paris', 20],
['EUR', 'FR', 'Lyon', 11.4],
['EUR', 'ES', 'Madrid', 8.9],
['GBP', 'UK', 'London', 12.2],
['FBP', 'UK', 'London', 10.9]
]


class Nester:
    pass


class NestingLevels:
    def validate():
        pass


class NestingLevelsData:
    pass


class Data:
    def load():
        pass

    def is_valid():
        self.validate()

    def validate():
        pass


class DataFromCommand:
    pass


class DataFromApi:
    pass
