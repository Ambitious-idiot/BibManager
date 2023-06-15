import uuid
import hashlib
import re
from tkinter import messagebox
from .page import *


@register_page()
class Register(Page):
    def __init__(self):
        self.username = tkinter.StringVar()
        self.email = tkinter.StringVar()
        self.password0 = tkinter.StringVar()
        self.password1 = tkinter.StringVar()
        components = [
            Component(tkinter.Label, {}, {'row': 0}),
            Component(tkinter.Label, {'text': '用户名'},
                      {'row': 1, 'stick': tkinter.W, 'pady': 10}),
            Component(tkinter.Entry, {'textvariable': self.username},
                      {'row': 1, 'column': 1, 'stick': tkinter.E}),
            Component(tkinter.Label, {'text': '邮箱'},
                      {'row': 2, 'stick': tkinter.W, 'pady': 10}),
            Component(tkinter.Entry, {'textvariable': self.email},
                      {'row': 2, 'column': 1, 'stick': tkinter.E}),
            Component(tkinter.Label, {'text': '密码'},
                      {'row': 3, 'stick': tkinter.W, 'pady': 10}),
            Component(tkinter.Entry, {'textvariable': self.password0, 'show': '*'},
                      {'row': 3, 'column': 1, 'stick': tkinter.E}),
            Component(tkinter.Label, {'text': '再次输入'},
                      {'row': 4, 'stick': tkinter.W, 'pady': 10}),
            Component(tkinter.Entry, {'textvariable': self.password1, 'show': '*'},
                      {'row': 4, 'column': 1, 'stick': tkinter.E}),
            Component(tkinter.Button, {'text': '返回', 'command': self.login},
                      {'row': 5, 'stick': tkinter.W, 'pady': 10}),
            Component(tkinter.Button, {'text': '注册', 'command': self.register},
                      {'row': 5, 'column': 1, 'stick': tkinter.E})
        ]
        super(Register, self).__init__('BibManager-Register', '400x250+600+300', components)

    def login(self):
        self.to('Login')

    def register(self):
        # Verify inputs
        password = self.password0.get()
        if password != self.password1.get():
            messagebox.showwarning('错误', '输入密码不相符')
            return
        if len(password) == 0:
            messagebox.showerror('错误', '密码不能为空')
            return
        username = self.username.get()
        if len(username) == 0:
            messagebox.showerror('错误', '用户名不能为空')
            return
        if len(username) > 15:
            messagebox.showerror('错误', '用户名长度小于等于15')
            return
        if re.match(r'^\w+$', username) is None:
            messagebox.showerror('错误', '用户名只包含字母、数字或下划线')
            return
        email = self.email.get()
        if len(email) == 0:
            messagebox.showerror('错误', '邮箱不能为空')
            return
        # Generate UID with username
        namespace = uuid.uuid4()
        uid = str(uuid.uuid5(namespace, username))
        # Generate sha256 of password
        pwd = self.sha256(password)
        # Insert new user to TABLE USER
        cursor = self.db.cursor()
        query = f"INSERT INTO USER VALUES ('{str(uid)}', '{username}', '{pwd}', '{email}')"
        try:
            cursor.execute(query)
            cursor.close()
            logging.info(query)
            self.db.commit()
            messagebox.showinfo("成功", "注册成功，按确定返回登录界面")
            self.to('Login')
        except sqlite3.IntegrityError:
            messagebox.showerror("注册失败", "该账户已存在")

    @staticmethod
    def sha256(password):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode('utf-8'))
        return sha256_hash.hexdigest()
