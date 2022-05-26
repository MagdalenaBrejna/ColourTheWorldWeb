from tkinter import *
from tkinter import messagebox
from flask import flash, render_template

class MyException(Exception):
    def __init__(self, value):
        self._value = value


class MyDialogException(MyException):
    def __init__(self, value):
        MyException.__init__(self, value)
        self.__create_dialog()

    def __create_dialog(self):
        self.__tk = Tk()
        self.__tk.withdraw()
        self.__tk.attributes('-topmost', True)

    def _show_dialog(self, tit, mess):
        messagebox.showerror(title = tit, message = mess) 
        self.__destroy_dialog()  

    def __destroy_dialog(self):
        self.__tk.destroy()    

class DownloadException(MyDialogException):
    def __init__(self, value):
        MyDialogException.__init__(self, value)
        self._show_dialog("Download Error", "File %s cannot be downloaded" % (self._value))


class MyFlashException(MyException):
    def __init__(self, value, page):
        MyException.__init__(self, value)
        self.__page = page
        self.__show_message()

    def __show_message(self):
        flash(self._value)
        return render_template(self.__page)    

class ImageException(MyFlashException):
    def __init__(self, value, page):
        MyFlashException.__init__(self, value, page)

class AuthenticationException(MyFlashException):
    def __init__(self, value):
        MyFlashException.__init__(self, value, "login.html")
