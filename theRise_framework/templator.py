from jinja2 import Template
from os.path import join


def render(template_name, folder='templates', **kwargs):
    file_path = join(folder, template_name)

    with open(file_path, encoding='utf-8') as file:
        template = Template(file.read())

    # рендер шаблона с параметрами
    return template.render(**kwargs)
