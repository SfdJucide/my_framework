from time import time
from colorama import Fore, init

init(autoreset=True)


# декоратор маршрутизации
class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


# декоратор информации о функции
class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def time_measure(*args, **kwargs):
                start = time()
                result = method(*args, **kwargs)
                stop = time()
                delta = stop - start

                print(Fore.LIGHTMAGENTA_EX + f'DEBUG >>> {self.name} done in {delta:2.2f} ms')
                return result

            return time_measure

        return timeit(cls)
