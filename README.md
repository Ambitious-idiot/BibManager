# README
数据库结课作业：基于TKinter与SQLite的文献管理系统，实现了用户注册与登录系统与文献管理系统。数据源为作者Zotero导出bibtex。
## 如何运行
打开终端运行以下命令
```shell
cd $PATH2PROJECT
sqlite3 bibliography.db
.read bib.sql
python main.py
```
## 基本功能
- 用户的注册和登录
- 查看用户个人文献库
- 添加或删除个人文献库内容
- 查看用户文献详情页
- 查看并修改用户文献详情
