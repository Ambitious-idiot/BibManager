import tkinter
import sqlite3
import logging
from os import path as osp
from typing import List, Dict, ClassVar


class Component:
    __slots__ = ('widget', 'args', 'place_args', 'placement')

    def __init__(self, widget: ClassVar[tkinter.Widget],
                 args: Dict, place_args: Dict, placement: str = 'grid'):
        self.widget = widget
        self.args = args
        self.place_args = place_args
        self.placement = placement

    def __call__(self, ui):
        if self.placement == 'grid':
            self.widget(ui, **self.args).grid(**self.place_args)
        elif self.placement == 'place':
            self.widget(ui, **self.args).place(**self.place_args)
        else:
            self.widget(ui, **self.args).pack(**self.place_args)


class Page:
    ui = tkinter.Tk()
    db = sqlite3.connect(osp.join(osp.dirname(__file__), '../bibliography.db'))
    logging.basicConfig(filename=osp.join(osp.dirname(__file__), '../log.txt'),
                        level=logging.INFO,
                        format='[%(asctime)s]: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    uid = ''
    user = 'test'

    def __init__(self, title: str, geometry: str, components: List[Component]):
        self.ui.title(title)
        self.ui.geometry(geometry)
        self.page = tkinter.Frame(self.ui)
        for component in components:
            component(self.page)
        self.page.pack()

    def to(self, page_name: str, *args, **kwargs):
        self.page.destroy()
        render(page_name, *args, **kwargs)

    @classmethod
    def mainloop(cls):
        return cls.ui.mainloop()

    @classmethod
    def close(cls):
        cls.db.close()


_REGISTRY = {}


def register_page():
    def decorator(cls: ClassVar[Page]):
        _REGISTRY[cls.__name__] = cls
        return cls
    return decorator


def render(name, *args, **kwargs):
    return _REGISTRY[name](*args, **kwargs)
