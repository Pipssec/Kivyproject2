import psycopg2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import StringProperty, ListProperty
from kivy.config import Config
import hashlib

Config.set('kivy', 'keyboard_mode', 'systemanddock')
switch_auth = []
profile_name = []


def connectdb():
    conn = psycopg2.connect(user="postgres",
                            password="qwerty",
                            host="127.0.0.1",
                            port="5432",
                            database='main')
    return conn


def switch_on():
    switch_auth.append(1)


def switch_off():
    switch_auth.clear()
    profile_name.clear()


class MenuScreen(Screen):
    pass


class AboutUs(Screen):
    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class FullInformation(Screen):
    name_order = StringProperty()
    town = StringProperty()
    full_text = StringProperty()
    order_obl = StringProperty()
    order_car = StringProperty()
    order_car_model = StringProperty()
    order_car_year = StringProperty()
    order_car_fuel = StringProperty()
    order_car_username = StringProperty()
    order_phone = StringProperty()

    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class ListOrders(Screen):
    data = ListProperty()

    def on_pre_enter(self):
        try:
            cursor = connectdb().cursor()
            try:
                cursor.execute('SELECT name_order FROM orders')
                orders = cursor.fetchall()
                cursor.execute('SELECT order_town FROM orders')
                towns = cursor.fetchall()
                for order, town in zip(orders, towns):
                    self.data.append(
                        {
                            "text": f'{order[0]} {town[0]}',
                            "on_release": lambda x=(order[0]): self.show_full_information(x)
                        }
                    )
                connectdb().close()
            except:
                pass
        except:
            sm.current = 'notsignal'

    def show_full_information(self, full_information):
        full_information_screen = sm.get_screen('fullinformation')
        cursor = connectdb().cursor()
        cursor.execute(f'SELECT * FROM orders WHERE name_order LIKE %s', (full_information,))
        information = cursor.fetchone()
        full_information_screen.name_order = information[0]
        full_information_screen.town = information[2]
        full_information_screen.full_text = information[1]
        full_information_screen.order_obl = information[3]
        full_information_screen.order_car = information[4]
        full_information_screen.order_car_model = information[5]
        full_information_screen.order_car_year = information[6]
        full_information_screen.order_car_fuel = information[7]
        full_information_screen.order_car_username = information[8]
        full_information_screen.order_phone = information[9]
        connectdb().close()
        sm.current = 'fullinformation'

    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"

    def on_leave(self):
        self.data.clear()





class NoSignal(Screen):
    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


kv = Builder.load_file("My.kv")

sm = ScreenManager(transition=FadeTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(AboutUs(name='about_us'))
sm.add_widget(ListOrders(name='list_orders'))
sm.add_widget(FullInformation(name='fullinformation'))
sm.add_widget(NoSignal(name='notsignal'))


class MyApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()
