from theRise_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from theRise_framework.utils.pre_filling_page import index_filling
from theRise_framework.utils.validators import name_validator
from patterns.structural_patterns import AppRoute, Debug

website = Engine()
logger = Logger('mainLogger')
routes = {}


@AppRoute(routes, url='/')
class Index:
    @Debug('index')
    def __call__(self, request):
        # наполнение сайта данными
        index_filling(website)

        return '200 OK', render('index.html',
                                date=request.get('date', None), title=request.get('title'),
                                categories=website.categories)


@AppRoute(routes, url='/contacts/')
class Contacts:
    @Debug('contacts')
    def __call__(self, request):
        return '200 OK', render('contacts.html', title=request.get('title'),
                                categories=website.categories)


@AppRoute(routes, url='/books/')
class Books:
    @Debug('book_list')
    def __call__(self, request):
        logger.log('Book list')
        try:
            category = website.get_category_by_id(int(request['request_params']['id']))
            logger.log(category.books)
            return '200 OK', render('books.html', title=request.get('title'),
                                    objects_list=category.books, categories=website.categories)

        except KeyError:
            logger.log(website.books)
            return '200 OK', render('books.html', title=request.get('title'),
                                    objects_list=website.books, categories=website.categories)


@AppRoute(routes, url='/create_book/')
class CreateBook:
    @Debug('create_book')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            # название книги
            name = data['name']
            name = website.decode_value(name)

            # автор книги
            author = data['author']
            author = website.decode_value(author)
            author, length = name_validator(author)
            website.authors.append(website.create_user('author', author[0], author[1])) if length == 2 \
                else website.authors.append(website.create_user('author', author[0]))

            # категория
            category_id = data['category']
            category = website.get_category_by_id(int(category_id))

            book = website.create_book('study', name, website.authors[-1], category)
            website.books.append(book)

            logger.log('Book has been successfully added')

            return '200 OK', render('books.html', title=request.get('title'),
                                    objects_list=website.books, categories=website.categories)

        else:
            if website.categories:
                return '200 OK', render('create_book.html', title=request.get('title'),
                                        categories=website.categories)
            else:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes, url='/create_category/')
class CreateCategory:
    @Debug('create_category')
    def __call__(self, request):
        logger.log('Category list')

        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = website.decode_value(name)

            category = website.create_category(name)
            website.categories.append(category)

            logger.log(website.categories)
            return '200 OK', render('create_category.html', title=request.get('title'),
                                    categories=website.categories)
        else:
            logger.log(website.categories)
            return '200 OK', render('create_category.html', title=request.get('title'),
                                    categories=website.categories)
