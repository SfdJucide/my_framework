from quopri import decodestring

from patterns.behavioral_patterns import Subject, FileWriter, ConsoleWriter


class User:
    auto_id = 0

    def __init__(self, first_name, last_name):
        self.id = self.auto_id
        User.auto_id += 1
        self.first_name = first_name
        self.last_name = last_name


class Author(User):
    pass


class Reader(User):
    def __init__(self, first_name, last_name):
        self.books = []
        super().__init__(first_name, last_name)


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


class Book(Subject):

    def __init__(self, name, author, category):
        self.name = name
        self.author = f'{author.first_name} {author.last_name}' if author.last_name else f'{author.first_name}'
        self.category = category.name
        category.books.append(self)
        self.readers = []
        super().__init__()

    def __getitem__(self, item):
        return self.readers[item]

    def add_reader(self, reader):
        self.readers.append(reader)
        print(self.readers)
        reader.books.append(self)
        print(reader.books)
        self.notify()


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
    def create_user(type_, first_name=None, last_name=None):
        return UserFactory.create(type_, first_name, last_name)

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_book(type_, name, author, category):
        return BookFactory.create(type_, name, author, category)

    def get_book(self, book_name):
        for book in self.books:
            if book.name == book_name:
                return book
        raise Exception(f'Книга не найдена!')

    def get_category_by_id(self, cat_id):
        for item in self.categories:
            if item.id == cat_id:
                return item
        raise Exception(f'Категории с id = {cat_id} не найдены!')

    def get_reader_by_id(self, user_id):
        for user in self.readers:
            if user.id == user_id:
                return user
        raise Exception(f'Пользователь с id = {user_id} не найден!')

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

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'LOG >>> {text}'
        self.writer.write(text)
