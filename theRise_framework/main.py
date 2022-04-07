from theRise_framework.errors.page_errors import PageNotFound404
from theRise_framework.utils.decode_utils import decode_value
from theRise_framework.requests import GetRequest, PostRequest, logger


class Framework:

    """ Главное приложения фреймворка """

    def __init__(self, routes_obj, fronts_obj):
        self.routes = routes_obj
        self.fronts = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес из словаря
        path = environ['PATH_INFO']

        # получаем тип запроса
        method = environ['REQUEST_METHOD']

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
        request['method'] = method

        if method == 'GET':
            request_params = GetRequest().get_request_params(environ)
            request['request_params'] = decode_value(request_params)
            logger.log(f'GET-параметры: {decode_value(request_params)}')
        elif method == 'POST':
            data = PostRequest().get_request_params(environ)
            request['data'] = decode_value(data)
            logger.log(f'POST-запрос: {decode_value(data)}')

        # отработка паттерна front controller
        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
