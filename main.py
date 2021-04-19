from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
from datetime import datetime

import os
import ast
import time


class MenuScreen(Screen):#START SCREEN
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')
        box.add_widget(Button(text='Список витрат',font_size=25, on_press=lambda x:
                              set_screen('list_money')))
        box.add_widget(Button(text='Додати витрати',font_size=25,
                              on_press=lambda x: set_screen('add_money')))
        self.add_widget(box)


class SortedListMoney(Screen):
    def __init__(self, **kw):
        super(SortedListMoney, self).__init__(**kw)

    def on_enter(self):  # функція визивається в момент відкриття екрану

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        back_button = Button(text='< Назад до головного меню',
                             on_press=lambda x: set_screen('menu'),
                             size_hint_y=None, height=dp(40))
        self.layout.add_widget(back_button)
        root = RecycleView(size_hint=(1, None), size=(Window.width,
                                                      Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)

        dic_money = ast.literal_eval(
            App.get_running_app().config.get('General', 'user_data'))

        for f, d in sorted(dic_money.items(), key=lambda x: x[1]):#Виводим список витрат
            fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime('%Y-%m-%d'))
            btn = Button(text=fd, size_hint_y=None, height=dp(40))

            self.layout.add_widget(btn)

    def on_leave(self):  # Функція буде викликана в момент закриття екрану

        self.layout.clear_widgets()  # при закритті чистимо список


class AddMoney(Screen): # Добавлення витрати в список

    def buttonClicked(self, btn1):# провіряєм чи пусті лейбли
        if not self.txt1.text:
            return
        elif not self.txt3.text:
            return

        self.text5=str(self.txt1.text+" "+self.txt3.text)
        self.app = App.get_running_app()
        self.app.user_data = ast.literal_eval(
            self.app.config.get('General', 'user_data'))
        self.app.user_data[self.text5.encode('u8')] = int(time.time())
        self.app.config.set('General', 'user_data', self.app.user_data)
        self.app.config.write()
        text = "Остання витрата:  " + self.txt1.text+" "+self.txt3.text
        self.result.text = text
        self.txt1.text = ''
        self.txt3.text = ''


    def __init__(self, **kw):# Cтворюєм вікно де будумо додавати витрати
        super(AddMoney, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')
        back_button = Button(text='< Назад до головного меню', on_press=lambda x:
                             set_screen('menu'), size_hint_y=None, height=dp(40))
        box.add_widget(back_button)
        self.txt1 = TextInput(text='', multiline=False, height=dp(40),
                              size_hint_y=None, hint_text="Cума витрати")

        self.txt3 = TextInput(text='', multiline=False, height=dp(40),
                              size_hint_y=None, hint_text="Валюта")
        box.add_widget(self.txt1)
        box.add_widget(self.txt3)

        btn1 = Button(text="Додати у список витрат", size_hint_y=None, height=dp(40))#добавляємо витрати
        btn1.bind(on_press=self.buttonClicked)
        box.add_widget(btn1)
        self.result = Label(text='')
        box.add_widget(self.result)
        self.add_widget(box)


def set_screen(name_screen):#задаєм еркан(ініцілізуєм)
    sm.current = name_screen


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SortedListMoney(name='list_money'))
sm.add_widget(AddMoney(name='add_money'))


class MyFinanceApp(App): #Настройки конфігурації
    def __init__(self, **kvargs):
        super(MyFinanceApp, self).__init__(**kvargs)
        self.config = ConfigParser()

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(MyFinanceApp, self).get_application_config(
            '{}/%(appname)s.ini'.format(self.directory))

    def build(self):
        return sm


if __name__ == '__main__':
    MyFinanceApp().run()
