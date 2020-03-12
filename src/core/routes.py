import typing as t
import importlib


class URLPattern:
    def __init__(self, method: str, path: str, handler, name: str = None, defaults=None) -> None:
        self.method = method
        self.path = path
        self.handler = handler
        self.name = name
        self.defaults = defaults or {}


def setup_routes(app, url_paths: t.Sequence[str]) -> None:
    patterns_list = [importlib.import_module(u).patterns for u in url_paths]

    for url_patterns in patterns_list:
        if not isinstance(url_patterns, (list, tuple)):
            raise RuntimeError('url pattern collection must be list or tuple.')

        if not url_patterns:
            continue

        for url_pattern in url_patterns:
            if not isinstance(url_pattern, URLPattern):
                raise RuntimeError(
                    'url pattern collection must be '
                    'URLPattern instance.'
                )

            app.add_url_rule(
                rule=url_pattern.path,
                view_func=url_pattern.handler,
                methods=[url_pattern.method],
                defaults=url_pattern.defaults,
            )


url = URLPattern
