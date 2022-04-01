from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):

    # создание объекта окружения
    env = Environment()
    # каталог для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # получаем сам шаблон
    template = env.get_template(template_name)

    return template.render(**kwargs)
