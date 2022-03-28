from wsgiref.simple_server import make_server

from theRise_framework.main import Framework
from urls import routes, fronts


application = Framework(routes, fronts)

# запуск приложения
with make_server('', 8080, application) as httpd:
    httpd.serve_forever()
