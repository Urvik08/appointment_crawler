import tornado
import tornado.web
import notification

MAX_RESPONSE_SIZE = 20 * 1024 * 1024 * 1024
MAX_BUFFER_SIZE = 1 * 1024 * 1024 * 1024


class HelloWorldHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write({"msg": "hello world"})


class SendTextHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        if not body:
            self.set_status(403)
        else:
            yield tornado.ioloop.IOLoop.current() \
                .run_in_executor(None, notification.send_text, body["title"],
                                 body["text"])
        self.flush()


class NotificationHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        if not body:
            self.set_status(403)
        else:
            yield tornado.ioloop.IOLoop.current() \
                .run_in_executor(None, notification.notify, body["title"],
                                 body["text"])
        self.flush()


class EmailHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        if not body:
            self.set_status(403)
        else:
            yield tornado.ioloop.IOLoop.current() \
                .run_in_executor(None, notification.email_to_user,
                                 body["title"],
                                 body["text"])
        self.flush()


def set_tcp_handler():
    tcp_handlers = [("/hello", HelloWorldHandler),
                    ("/notify", NotificationHandler),
                    ("/text", SendTextHandler),
                    ("/email", EmailHandler)]
    tcp_app = tornado.web.Application(tcp_handlers)
    http_server = \
        tornado.httpserver.HTTPServer(tcp_app,
                                      max_buffer_size=MAX_BUFFER_SIZE,
                                      max_body_size=MAX_RESPONSE_SIZE)
    http_server.listen(4545, address="0.0.0.0")


if __name__ == '__main__':
    try:
        set_tcp_handler()
        print("Starting on host server")
        tornado.ioloop.IOLoop.current().start()

    except Exception as ex:
        print("Exception starting tornado server: {}".format(ex))
