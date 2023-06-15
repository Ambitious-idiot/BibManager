from .page import *
from datetime import datetime


status_mapper = ('已读', '未读', '想读')


@register_page()
class PaperInfo(Page):
    # noinspection PyTypeChecker
    def __init__(self, args):
        pid, title, year, pub, url, reference, _, _, status, time, tag = args
        self.pid = pid
        super(PaperInfo, self).__init__(f'BibManager-{title}', '700x700+300+50', [])
        self.__delattr__('page')
        self.heading = tkinter.Label(self.ui, text=title, font=('Times New Roman', 25), wraplength=500)
        self.heading.pack(side=tkinter.TOP, pady=10)

        def _cmd(_key, _value):
            def func():
                self.to('UpdateInfo', _key, _value, pid, title)
            return func

        self.keys = [tkinter.Button(self.ui, text=text, font=('宋体', 15), command=cmd) for (text, cmd) in zip(
                ['发表', '年份', '标签', '被引用', 'URL', '状态'],
                [_cmd(key, value) for key, value in zip(
                    ['PUB', 'YEAR', 'TAG', 'REFERENCE', 'URL', 'STATUS'],
                    [pub, year, tag, reference, url, status]
                )])]
        for index, key in enumerate(self.keys):
            key.place(relx=0.1, rely=0.27 + index * 0.07, relwidth=0.15)
        self.keys.append(tkinter.Label(self.ui, text='上次浏览', font=('宋体', 15)))
        self.keys[-1].place(relx=0.1, rely=0.69, relwidth=0.15)
        self.values = [tkinter.Label(self.ui, text=text, font=('宋体', 15), wraplength=350) for
                       text in [pub, year, tag, reference, url, status_mapper[status], time]]
        for index, value in enumerate(self.values):
            value.place(relx=0.5, rely=0.27 + index * 0.07, relwidth=0.5, relheight=0.07)
        cursor = self.db.cursor()
        query = f"SELECT AUTHOR.NAME FROM WRITE, AUTHOR WHERE WRITE.PID='{self.pid}' AND WRITE.AID=AUTHOR.AID"
        cursor.execute(query)
        authors = cursor.fetchall()
        cursor.close()

        def _author(_authors):
            def func():
                self.to('Author', authors, pid, title)
            return func

        self.author = tkinter.Button(self.ui, text='作者', font=('宋体', 15), command=_author(authors))
        self.author.place(relx=0.1, rely=0.2, relwidth=0.15)
        self.first_author = tkinter.Label(self.ui, text=authors[0][0]+' et al.' if len(authors) != 0 else '',
                                          font=('宋体', 15), wraplength=350)
        self.first_author.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.07)

        self.mainpage = tkinter.Button(self.ui, text='返回主页',
                                       font=('宋体', 15), command=self._mainpage)
        self.mainpage.place(relx=0.3, rely=0.85, relwidth=0.3)

    def to(self, page_name: str, *args, **kwargs):
        self.heading.destroy()
        self.author.destroy()
        self.first_author.destroy()
        for key in self.keys:
            key.destroy()
        for value in self.values:
            value.destroy()
        time = datetime.today().strftime("%Y-%m-%d")
        cursor = self.db.cursor()
        query = f"UPDATE READ SET TIME='{time}' WHERE PID='{self.pid}' AND UID='{self.uid}'"
        cursor.execute(query)
        cursor.close()
        logging.info(query)
        self.db.commit()
        self.mainpage.destroy()
        render(page_name, *args, **kwargs)

    def _mainpage(self):
        self.to('MainPage')
