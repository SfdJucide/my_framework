from datetime import date

from views import Index, Contacts, Examples


# front controllers
def date_front(request):
    request['date'] = date.today()


def title_front(request):
    request['title'] = 'theRise'


fronts = [date_front, title_front]

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    '/examples/': Examples(),
}
