import hashlib
import re
from tkinter import messagebox
from .page import *


@register_page()
class Login(Page):
    def __init__(self):
        self.username = tkinter.StringVar()
        self.pwd = tkinter.StringVar()
        components = [
            Component(tkinter.Label, {}, {'row': 0}),
            Component(tkinter.Label, {'text': '用户名/邮箱'},
                      {'row': 1, 'stick': tkinter.W, 'pady': 10}),
            Component(tkinter.Entry, {'textvariable': self.username},
                      {'row': 1, 'column': 1, 'stick': tkinter.E}),
            Component(tkinter.Label, {'text': '密码'},
                      {'row': 2, 'stick': tkinter.W, 'pady': 10}),
            Component(tkinter.Entry, {'textvariable': self.pwd, 'show': '*'},
                      {'row': 2, 'column': 1, 'stick': tkinter.E}),
            Component(tkinter.Button, {'text': '登录', 'command': self.login},
                      {'row': 3, 'stick': tkinter.W, 'pady': 10}),
            Component(tkinter.Button, {'text': '注册账号', 'command': self.register},
                      {'row': 3, 'column': 1, 'stick': tkinter.E})
        ]
        super(Login, self).__init__('BibManager-Login', '400x200+600+300', components)

    def register(self):
        self.to('Register')

    def login(self):
        # Verify username existence
        username = self.username.get()
        cursor = self.db.cursor()
        if re.match(r'^\w+$', username) is not None:
            query = 'SELECT UID, USERNAME, PASSWORD FROM USER WHERE USERNAME=?'
        else:
            query = 'SELECT UID, USERNAME, PASSWORD FROM USER WHERE EMAIL=?'
        cursor.execute(query, [username])
        c = cursor.fetchall()
        cursor.close()
        if len(c) == 0:
            messagebox.showerror('登录失败', '账户不存在')
            return
        # Verify the password
        uid, user, pwd = c[0]
        if self.sha256(self.pwd.get()) != pwd:
            messagebox.showwarning('登录失败', '密码错误')
            return
        # Welcome the user
        Page.uid = uid
        Page.user = user
        messagebox.showinfo('登录成功', '欢迎：%s' % user)
        self.to('MainPage')

    @staticmethod
    def sha256(password):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode('utf-8'))
        return sha256_hash.hexdigest()
