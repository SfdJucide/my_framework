from theRise_framework.errors.page_errors import PageNotFound404


class Framework:

    """ Главное приложения фреймворка """

    def __init__(self, routes_obj, fronts_obj):
        self.routes = routes_obj
        self.fronts = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес из словаря
        path = environ['PATH_INFO']

        # проверка наличия слеша в конце пути
        if not path.endswith('/'):
            path = f'{path}/'

        # отработка паттерна page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # request словарь получает все контроллеры
        request = {}

        # отработка паттерна front controller
        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
