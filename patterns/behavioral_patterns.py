from colorama import init, Fore
from jsonpickle import dumps, loads

from theRise_framework.templator import render

init(autoreset=True)


# паттерн - наблюдатель
class Observer:

    def update(self, book):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):
    def update(self, subject):
        print(Fore.BLUE + 'SMS >>>', subject.readers[-1].first_name, f'starts read {subject.name}')


class EmailNotifier(Observer):
    def update(self, subject):
        print(Fore.CYAN + 'EMAIL >>>', subject.readers[-1].first_name, f'starts read {subject.name}')


# паттерн хранитель
class Serializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


# паттерн - стратегия
class ConsoleWriter:

    @staticmethod
    def write(text):
        print(Fore.LIGHTYELLOW_EX + text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


# паттерн - Шаблонный метод
class TemplateView:
    template_name = '#'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':

            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)
