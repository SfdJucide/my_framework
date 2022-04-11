from datetime import date

# from views import Index, Contacts, Books, CreateBook, CreateCategory


# front controllers
def date_front(request):
    request['date'] = date.today()


def title_front(request):
    request['title'] = 'theRise'


fronts = [date_front, title_front]

# routes = {
#     '/': Index(),
#     '/contacts/': Contacts(),
#     '/books/': Books(),
#     '/create_book/': CreateBook(),
#     '/create_category/': CreateCategory(),
# }
