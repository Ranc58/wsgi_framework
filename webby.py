import socket


class App:
    urls = {}

    def __init__(self):
        self.client_connection = None
        self.client_address = None

    def run_server(self, host='localhost', port=9005):
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_socket.bind((host, port))
        serv_socket.listen()
        while True:
            self.client_connection, self.client_address = serv_socket.accept()
            parsed_request = self._parse_request(
                self.client_connection.recv(1024))
            if parsed_request:
                self._response(parsed_request)

    def _parse_request(self, request):
        if request:
            headers = request.decode("utf-8").splitlines()
            first_line = headers.pop(0)
            (verb, url, version) = first_line.split()
            parsed_request = {'method': verb, 'url': url, 'version': version}
            for h in headers:
                h = h.split(': ')
                if len(h) < 2:
                    continue
                field = h[0]
                value = h[1]
                parsed_request[field] = value
            return parsed_request

    def _response(self, parsed_request):
        if parsed_request['url'] in self.urls:
            content = self.urls.get(parsed_request['url'])
            response = '{version} 200 OK\n\n {content}'.format(
                version=parsed_request['version'], content=content
            )
        else:
            response = '{version} 404 Not Found\n\nNot found!'.format(
                version=parsed_request['version'])
        self.client_connection.sendall(str.encode(response))
        self.client_connection.close()

    def add_to_url_map(self, url):
        def wrapper(func):
            if url not in self.urls:
                response = func()
                self.urls.update({url: response})
        return wrapper
