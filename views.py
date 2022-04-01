from theRise_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None), title=request.get('title'))


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', title=request.get('title'))


class Examples:
    def __call__(self, request):
        return '200 OK', render('examples.html', title=request.get('title'))
