class PageNotFound404:
    def __call__(self, request):
        return '404 Error', '404 PAGE Not Found'
