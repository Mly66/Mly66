from tkinter import *
from tkinter.messagebox import *
import pymysql
from tkinter import ttk
import time

# 数据库连接信息
host = '127.0.0.1'
username = 'root'
password = 'root'
db = 'test'

# 主界面类
class MainPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小
        self.createPage()

    # 创建主界面
    def createPage(self):
        self.inputPage = InputFrame(self.root)  # 创建不同Frame
        self.inputPage.pack()  # 默认显示数据录入界面

    def inputData(self):
        self.inputPage.pack()

# 登录界面类
class LoginPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (300, 180))  # 设置窗口大小
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    # 创建登录界面
    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='账户: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=3, column=1, stick=E)

    # 登录验证函数
    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()
        if name == 'admin' and secret == 'admin':
            self.page.destroy()
            MainPage(self.root)
        else:
            showinfo(title='错误', message='账号或密码错误！')

# 数据录入界面类
class InputFrame(Frame):
    def __init__(self, master=None):
        # 连接数据库
        self.conn = pymysql.connect(host=host, user=username, password=password, database=db)
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.kind = StringVar()
        self.age = StringVar()
        self.sex = StringVar()
        self.health = StringVar()
        self.sinkness = StringVar()
        self.color = StringVar()
        self.createPage()

    # 查询流浪狗信息
    def search(self):
        root1 = Tk()
        root1.title('查询流浪狗信息')
        cursor = self.conn.cursor()
        sql = "select id,kind,age,sex,health,sinkness,color from dog_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        tree = ttk.Treeview(root1, columns=["编号", "种类", "年龄", "性别", "健康状况", "疾病史", "颜色"], show='headings')  # 表格
        tree.column("编号", width=60)
        tree.column("种类", width=60)
        tree.column("年龄", width=60)
        tree.column("性别", width=60)
        tree.column("健康状况", width=80)
        tree.column("疾病史", width=60)
        tree.column("颜色", width=60)
        tree.heading("编号", text="编号")
        tree.heading("种类", text="种类")
        tree.heading("年龄", text="年龄")
        tree.heading("性别", text="性别")
        tree.heading("健康状况", text="健康状况")
        tree.heading("疾病史", text="疾病史")
        tree.heading("颜色", text="颜色")
        for i in result:
            tree.insert('', 'end', values=i)
        tree.pack()

    # 插入流浪狗信息
    def insert(self):
        kind = self.kind.get()
        age = self.age.get()
        sex = self.sex.get()
        health = self.health.get()
        sinkness = self.sinkness.get()
        color = self.color.get()
        cursor = self.conn.cursor()
        sql = "insert into dog_info (kind,age,sex,health,sinkness,color) values ('%s','%s','%s','%s','%s','%s')" % (kind, age, sex, health, sinkness, color)
        cursor.execute(sql)
        self.conn.commit()
        showinfo(title='hi', message='录入成功')
        self.kind.set('')
        self.age.set('')
        self.sex.set('')
        self.health.set('')
        self.sinkness.set('')
        self.color.set('')

    # 修改流浪狗信息
    def update(self):
        def togengxin():
            kind = b4.get()
            did = b2.get()
            age = b6.get()
            health = b10.get()
            sex = b8.get()
            sinkness = b12.get()
            color = b14.get()
            cursor = self.conn.cursor()
            sql = "update dog_info set kind='%s',age='%s',sex= '%s' ,health='%s', sinkness='%s', color='%s' where id = '%s'" % (kind, age, sex, health, sinkness, color, did)
            cursor.execute(sql)
            self.conn.commit()
            showinfo(title='hi', message='修改成功')
            root1.destroy()

        root1 = Tk()
        root1.title('修改流浪狗信息')
        root1.geometry('300x400')
        did = StringVar()
        kind = StringVar()
        age = StringVar()
        health = StringVar()
        sex = StringVar()
        sinkness = StringVar()
        color = StringVar()
        b1 = Label(root1, text='请输入要修改狗狗的编号: ')
        b1.pack()
        b2 = Entry(root1, textvariable=did)
        b2.pack()
        b3 = Label(root1, text='请输入要修改狗狗的品种: ')
        b3.pack()
        b4 = Entry(root1, textvariable=kind)
        b4.pack()
        b5 = Label(root1, text='请输入要修改狗狗的年龄: ')
        b5.pack()
        b6 = Entry(root1, textvariable=age)
        b6.pack()
        b7 = Label(root1, text='请输入要修改狗狗的性别: ')
        b7.pack()
        b8 = Entry(root1, textvariable=sex)
        b8.pack()
        b9 = Label(root1, text='请输入要修改狗狗的身体状况: ')
        b9.pack()
        b10 = Entry(root1, textvariable=health)
        b10.pack()
        b11 = Label(root1, text='请输入要修改狗狗的疾病史: ')
        b11.pack()
        b12 = Entry(root1, textvariable=sinkness)
        b12.pack()
        b13 = Label(root1, text='请输入要修改狗狗的颜色: ')
        b13.pack()
        b14 = Entry(root1, textvariable=color)
        b14.pack()
        btn = Button(root1, text='修改',  command=togengxin)
        btn.pack()
        root1.mainloop()

    # 删除流浪狗信息
    def delete(self):
        def todelete():
            kind = b2.get()
            cursor = self.conn.cursor()
            sql = "delete from dog_info where id = '%s'" % (kind)
            cursor.execute(sql)
            self.conn.commit()
            showinfo(title='hi', message='删除成功')
            root1.destroy()

        root1 = Tk()
        root1.title('删除流浪狗信息')
        root1.geometry('300x200')
        kind = StringVar()
        b1 = Label(root1, text='请输入要删除狗狗的编号: ')
        b1.pack()
        b2 = Entry(root1, textvariable=kind)
        b2.pack()
        btn = Button(root1, text='删除',  command=todelete)
        btn.pack()
        root1.mainloop()

    # 领养流浪狗
    def lingyang(self):
        def tolingyang():
            kind = b2.get()
            name = b4.get()
            phone = b6.get()
            sex = b8.get()
            addr = b10.get()
            cursor = self.conn.cursor()
            now = time.strftime("%Y-%m-%d", time.localtime())
            sql = "insert into dog_lose values ('%s','%s','%s')" % (kind, now, addr)
            cursor.execute(sql)
            sql = "insert into dog_adopt values ('%s','%s','%s','%s','%s')" % (name, phone, sex, addr, kind)
            cursor.execute(sql)
            sql = "delete from dog_info where id = '%s'" % (kind)
            cursor.execute(sql)
            self.conn.commit()
            showinfo(title='hi', message='领养成功')
            root1.destroy()

        root1 = Tk()
        root1.title('领养流浪狗')
        root1.geometry('300x400')
        kind = StringVar()
        name = StringVar()
        phone = StringVar()
        sex = StringVar()
        addr = StringVar()
        b1 = Label(root1, text='请输入要领养狗狗的编号: ')
        b1.pack()
        b2 = Entry(root1, textvariable=kind)
        b2.pack()
        b3 = Label(root1, text='请输入领养人姓名: ')
        b3.pack()
        b4 = Entry(root1, textvariable=name)
        b4.pack()
        b5 = Label(root1, text='请输入领养人电话: ')
        b5.pack()
        b6 = Entry(root1, textvariable=phone)
        b6.pack()
        b7 = Label(root1, text='请输入领养人性别: ')
        b7.pack()
        b8 = Entry(root1, textvariable=sex)
        b8.pack()
        b9 = Label(root1, text='请输入领养人地址: ')
        b9.pack()
        b10 = Entry(root1, textvariable=addr)
        b10.pack()
        btn = Button(root1, text='领养',  command=tolingyang)
        btn.pack()
        root1.mainloop()

    # 创建数据录入界面
    def createPage(self):
        Button(self, text='查询流浪狗信息', command=self.search).grid(row=1, column=1, stick=E, pady=10)
        Button(self, text='修改流浪狗信息', command=self.update).grid(row=1, column=2, stick=E, pady=10)
        Button(self, text='领养流浪狗', command=self.lingyang).grid(row=1, column=3, stick=E, pady=10)
        Button(self, text='删除流浪狗信息', command=self.delete).grid(row=1, column=4, stick=E, pady=10)
        Label(self, text='狗狗品种: ').grid(row=3, column=2, stick=W, pady=10)
        Entry(self, textvariable=self.kind).grid(row=3, column=3, stick=E)
        Label(self, text='狗狗年龄: ').grid(row=4, column=2, stick=W, pady=10)
        Entry(self, textvariable=self.age).grid(row=4, column=3, stick=E)
        Label(self, text='狗狗性别: ').grid(row=5, column=2, stick=W, pady=10)
        Entry(self, textvariable=self.sex).grid(row=5, column=3, stick=E)
        Label(self, text='狗狗身体状况: ').grid(row=6, column=2, stick=W, pady=10)
        Entry(self, textvariable=self.health).grid(row=6, column=3, stick=E)
        Label(self, text='狗狗疾病史: ').grid(row=7, column=2, stick=W, pady=10)
        Entry(self, textvariable=self.sinkness).grid(row=7, column=3, stick=E)
        Label(self, text='狗狗颜色: ').grid(row=8, column=2, stick=W, pady=10)
        Entry(self, textvariable=self.color).grid(row=8, column=3, stick=E)
        Button(self, text='录入', command=self.insert).grid(row=10, column=3, stick=E, pady=10)

# 创建登录界面并运行主程序
root = Tk()
root.title('流浪狗救助管理系统')
LoginPage(root)
root.mainloop()
