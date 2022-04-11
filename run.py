from wsgiref.simple_server import make_server

from theRise_framework.main import Framework
from views import routes
from urls import fronts


application = Framework(routes, fronts)

# запуск приложения
with make_server('', 8080, application) as httpd:
    httpd.serve_forever()
