from werkzeug.serving import WSGIRequestHandler

from libs import FormatLogger

__all__ = ("CustomRequestHandler",)


class CustomRequestHandler(WSGIRequestHandler):
    # Just like WSGIRequestHandler, but without "- -"
    # noinspection PyShadowingBuiltins
    def log(self, type, message, *args):
        getattr(FormatLogger, type)("Request", message % args)
