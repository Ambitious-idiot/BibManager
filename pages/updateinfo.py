from .page import *


mapper = {
    'PUB': '发表',
    'YEAR': '年份',
    'TAG': '标签',
    'REFERENCE': '被引用',
    'URL': 'URL',
    'STATUS': '状态',
    'TIME': '上次浏览'
}


status_mapper = ('已读', '未读', '想读')


@register_page()
class UpdateInfo(Page):
    def __init__(self, key, value, pid, title):
        self.pid = pid
        self.key = key
        self.title = title
        super(UpdateInfo, self).__init__(f'BibManager-{title}-{mapper[key]}', '700x700+300+50', [])
        self.__delattr__('page')
        self.heading = tkinter.Label(self.ui, text=title, font=('Times New Roman', 25), wraplength=500)
        self.heading.pack(side=tkinter.TOP, pady=10)
        self.left = tkinter.Label(self.ui, text=mapper[key], font=('宋体', 15))
        self.left.place(relx=0.1, rely=0.4, relwidth=0.15)
        if key == 'STATUS':
            self.status_var = tkinter.StringVar()
            self.status_var.set(status_mapper[value])
            self.right = tkinter.OptionMenu(self.ui, self.status_var, *status_mapper)
            self.right.place(relx=0.4, rely=0.4, relwidth=0.55)
        else:
            self.right = tkinter.Text(self.ui, font=('Times New Roman', 15))
            self.right.place(relx=0.4, rely=0.15, relwidth=0.55, relheight=0.6)
            self.right.insert(tkinter.END, value if value else '')
        if key == 'URL':
            from webbrowser import open

            def _browse():
                if self.right.get('1.0', tkinter.END) != '':
                    open(self.right.get('1.0', tkinter.END))

            self.confirm = tkinter.Button(self.ui, text='前往', font=('宋体', 15), command=_browse)
            self.confirm.place(relx=0.15, rely=0.8, relwidth=0.3)
        else:
            self.confirm = tkinter.Button(self.ui, text='确定修改', font=('宋体', 15), command=self._update)
            self.confirm.place(relx=0.15, rely=0.8, relwidth=0.3)
        self.info = tkinter.Button(self.ui, text='返回', font=('宋体', 15), command=self._paper_info)
        self.info.place(relx=0.55, rely=0.8, relwidth=0.3)

    def _paper_info(self):
        cursor = self.db.cursor()
        query = 'SELECT * FROM PAPER, READ WHERE PAPER.PID=? AND ' \
                'PAPER.PID=READ.PID AND READ.UID=?'
        values = [self.pid, self.uid]
        cursor.execute(query, values)
        c = cursor.fetchone()
        cursor.close()
        self.to('PaperInfo', c)

    def _update(self):
        if self.key == 'STATUS':
            value = status_mapper.index(self.status_var.get())
        else:
            value = self.right.get('1.0', tkinter.END).strip()
        if self.key not in ['STATUS', 'YEAR', 'REFERENCE']:
            value = f"'{value}'"
        cursor = self.db.cursor()
        if self.key in ['PUB', 'YEAR', 'REFERENCE']:
            query = f"UPDATE PAPER SET {self.key}={value} WHERE PID='{self.pid}'"
            cursor.execute(query)
        else:
            query = f"UPDATE READ SET {self.key}={value} WHERE PID='{self.pid}' AND UID='{self.uid}'"
            cursor.execute(query)
        cursor.close()
        logging.info(query)
        self.db.commit()
        if self.key not in ['STATUS', 'YEAR', 'REFERENCE']:
            value = value[1:-1]
        self.to('UpdateInfo', self.key, value, self.pid, self.title)

    def to(self, page_name: str, *args, **kwargs):
        self.heading.destroy()
        self.left.destroy()
        self.right.destroy()
        self.info.destroy()
        self.confirm.destroy()
        render(page_name, *args, **kwargs)
