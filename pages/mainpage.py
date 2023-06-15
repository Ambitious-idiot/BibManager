from tkinter import ttk
from tkinter import messagebox
from .page import *


@register_page()
class MainPage(Page):
    def __init__(self):
        super(MainPage, self).__init__('BibManager', '700x700+300+50', [])
        self.page.destroy()
        self.__delattr__('page')
        self.clicked = None
        self.heading = tkinter.Label(self.ui, text='BibManager', fg='blue', font=('Forte', 30))
        self.heading.pack(side=tkinter.TOP, pady=10)
        self.welcome = tkinter.Label(self.ui, text=f'欢迎：{self.user}', fg='blue', font=('FiraCode Nerd Font', 10))
        self.welcome.pack(side=tkinter.TOP, anchor='ne', padx=20)
        self.pids = []
        headings = ['标题', '发表', '年份', '标签']
        self.data = ttk.Treeview(self.ui, show='headings',
                                 columns=headings)
        for heading in headings:
            self.data.column(heading, width=100, anchor='center')
            self.data.heading(heading, text=heading)
        self.data.place(rely=0.2, relwidth=0.97)
        self.data.bind('<Double-Button-1>', self.full_info)
        self.data.bind('<ButtonRelease-1>', self.get_clicked)
        self.get_info()
        self.adding = False
        self.add = tkinter.Button(self.ui, text="添加信息", command=self.add_info, font=('宋体', 15))
        self.add.place(relx=0.2, rely=0.6, relwidth=0.3)
        self.add_pid = tkinter.StringVar()
        self.entry = tkinter.Entry(textvariable=self.add_pid)
        self.delete = tkinter.Button(self.ui, text="删除信息", command=self.delete_info, font=('宋体', 15))
        self.delete.place(relx=0.5, rely=0.6, relwidth=0.3)

    def to(self, page_name: str, *args, **kwargs):
        self.data.destroy()
        self.heading.destroy()
        self.welcome.destroy()
        self.add.destroy()
        self.delete.destroy()
        render(page_name, *args, **kwargs)

    def get_info(self):
        cursor = self.db.cursor()
        query = 'SELECT PAPER.PID, PAPER.TITLE, PAPER.PUB, PAPER.YEAR, READ.TAG ' \
                'FROM PAPER, READ WHERE READ.UID = ? AND PAPER.PID=READ.PID'
        values = (self.uid,)
        cursor.execute(query, values)
        items = cursor.fetchall()
        for item in items:
            self.data.insert('', 1, text='line1', values=item[1:])
            self.pids.append(item[0])
        cursor.close()

    def full_info(self, _):
        pid = self.pids[self.data.index(self.data.selection()[0])]
        cursor = self.db.cursor()
        query = 'SELECT * FROM PAPER, READ WHERE PAPER.PID=? AND ' \
                'PAPER.PID=READ.PID AND READ.UID=?'
        values = [pid, self.uid]
        cursor.execute(query, values)
        c = cursor.fetchone()
        cursor.close()
        self.to('PaperInfo', c)

    def get_clicked(self, _):
        self.clicked = self.pids[self.data.index(self.data.selection()[0])]

    def delete_info(self):
        if self.clicked is None:
            messagebox.showerror("删除失败", "未选中任何表项")
            return
        cursor = self.db.cursor()
        query = f"DELETE FROM READ WHERE UID='{self.uid}' AND PID='{self.clicked}'"
        cursor.execute(query)
        cursor.close()
        logging.info(query)
        self.db.commit()
        messagebox.showinfo("删除成功", '删除成功')
        self.to('MainPage')

    def add_info(self):
        if self.adding:
            add_pid = self.add_pid.get()
            cursor = self.db.cursor()
            query = f"INSERT INTO READ VALUES ('{self.uid}', '{add_pid}', 1, NULL, '')"
            cursor.execute(query)
            cursor.close()
            logging.info(query)
            self.db.commit()
            messagebox.showinfo('添加成功', '添加成功')
            self.entry.destroy()
            self.to('MainPage')
            return
        self.entry.place(relx=0.2, rely=0.55)
        self.adding = True
