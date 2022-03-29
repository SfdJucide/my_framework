class Request:

    @staticmethod
    def parse_input_data(data: str) -> dict:
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                key, value = item.split('=')
                result[key] = value

        return result


class GetRequest(Request):

    def get_request_params(self, environ: dict) -> dict:
        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        return request_params


class PostRequest(Request):

    @staticmethod
    def get_wsgi_input_data(environ: dict) -> bytes:
        content_data_len = environ.get('CONTENT_LENGTH')
        content_length = int(content_data_len) if content_data_len else 0
        print(f'длинна пришедшей строки - {content_length}')

        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            print(f'строка после декодирования - {data_str}')
            result = self.parse_input_data(data_str)

        return result

    def get_request_params(self, environ: dict) -> dict:
        # полученные данные переводим в байты
        # затем обратно в словарь
        return self.parse_wsgi_input_data(self.get_wsgi_input_data(environ))
