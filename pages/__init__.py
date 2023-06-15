from .page import render


def _register_pages():
    from .login import Login
    from .register import Register
    from .mainpage import MainPage
    from .paperinfo import PaperInfo
    from .updateinfo import UpdateInfo
    from .author import Author

_register_pages()
del _register_pages

__all__ = [
    'render'
]
