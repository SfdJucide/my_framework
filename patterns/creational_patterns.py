from quopri import decodestring
from colorama import Fore, init

init(autoreset=True)


class User:

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Author(User):
    pass


class Reader(User):
    pass


# паттерн фабрика
class UserFactory:
    types = {
        'author': Author,
        'reader': Reader,
    }

    @classmethod
    def create(cls, type_, first_name, last_name):
        return cls.types[type_](first_name, last_name)


class Category:
    auto_id = 0

    def __init__(self, name):
        self.id = self.auto_id
        Category.auto_id += 1
        self.name = name
        self.books = []


class Book:

    def __init__(self, name, author, category):
        self.name = name
        self.author = f'{author.first_name} {author.last_name}'
        self.category = category.name
        category.books.append(self)


class ScientificBook(Book):
    pass


class StudyBook(Book):
    pass


class ReferenceBook(Book):
    pass


# паттерн фабрика
class BookFactory:
    types = {
        'study': StudyBook,
        'reference': ReferenceBook,
        'scientific': ScientificBook,
    }

    @classmethod
    def create(cls, type_, name, author, category):
        return cls.types[type_](name, author, category)


class Engine:

    def __init__(self):
        self.books = []
        self.authors = []
        self.readers = []
        self.categories = []

    @staticmethod
    def create_user(type_, first_name, last_name):
        return UserFactory.create(type_, first_name, last_name)

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_book(type_, name, author, category):
        return BookFactory.create(type_, name, author, category)

    def get_category_by_id(self, cat_id):
        for item in self.categories:
            if item.id == cat_id:
                return item
        raise Exception(f'Категории с id = {cat_id} не найдены!')

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print(Fore.LIGHTYELLOW_EX + 'LOG >>>', text)
