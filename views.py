from theRise_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from theRise_framework.utils.pre_filling_page import index_filling

website = Engine()
logger = Logger('mainLogger')


class Index:
    def __call__(self, request):
        # наполнение сайта данными
        index_filling(website)

        return '200 OK', render('index.html',
                                date=request.get('date', None), title=request.get('title'),
                                categories=website.categories)


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', title=request.get('title'),
                                categories=website.categories)


class Books:
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


class CreateBook:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            # название книги
            name = data['name']
            name = website.decode_value(name)

            # автор книги
            author = data['author']
            author = website.decode_value(author)
            website.authors.append(website.create_user('author', author.split()[0], author.split()[1]))

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


class CreateCategory:
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
