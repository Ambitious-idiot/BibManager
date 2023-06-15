from .page import *


@register_page()
class Author(Page):
    def __init__(self, authors, pid, title):
        self.pid = pid
        self.title = title
        self.authors = [author[0] for author in authors]
        super(Author, self).__init__(f'BibManager-{title}-作者', '700x700+300+50', [])
        self.__delattr__('page')
        self.heading = tkinter.Label(self.ui, text=title, font=('Times New Roman', 25), wraplength=500)
        self.heading.pack(side=tkinter.TOP, pady=10)
        self.left = tkinter.Label(self.ui, text='作者', font=('宋体', 15))
        self.left.place(relx=0.1, rely=0.4, relwidth=0.15)

        self.right = tkinter.Text(self.ui, font=('Times New Roman', 15))
        self.right.place(relx=0.4, rely=0.15, relwidth=0.55, relheight=0.6)
        value = ', '.join(author[0] for author in authors)
        self.right.insert(tkinter.END, value if value else '')
        self.confirm = tkinter.Button(self.ui, text='添加', font=('宋体', 15), command=self._update)
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

    def to(self, page_name: str, *args, **kwargs):
        self.heading.destroy()
        self.left.destroy()
        self.right.destroy()
        self.info.destroy()
        self.confirm.destroy()
        render(page_name, *args, **kwargs)

    def _update(self):
        authors = self.right.get('1.0', tkinter.END).strip().split(', ')
        for author in self.authors:
            if author not in authors:
                cursor = self.db.cursor()
                query = f"DELETE FROM WRITE WHERE PID='{self.pid}' AND AID='{author}'"
                cursor.execute(query)
                cursor.close()
                logging.info(query)
                self.db.commit()

        for author in authors:
            if author not in self.authors:
                cursor = self.db.cursor()
                query = f"SELECT * FROM AUTHOR WHERE NAME='{author}'"
                cursor.execute(query)
                c = cursor.fetchall()
                cursor.close()
                if len(c) == 0:
                    import hashlib
                    sha256_hash = hashlib.sha256()
                    sha256_hash.update(author.encode('utf-8'))
                    aid = sha256_hash.hexdigest()
                    cursor = self.db.cursor()
                    query = f"INSERT INTO AUTHOR VALUES ('{aid}', '{author}')"
                    cursor.execute(query)
                    cursor.close()
                    logging.info(query)
                    self.db.commit()
                cursor = self.db.cursor()
                query = f"INSERT INTO WRITE VALUES ('{self.pid}', '{author}')"
                cursor.execute(query)
                cursor.close()
                logging.info(query)
                self.db.commit()
        self.to('Author', authors, self.pid, self.title)
