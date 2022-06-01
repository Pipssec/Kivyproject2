from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition, FallOutTransition
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.config import Config
import sqlite3
import hashlib

Config.set('kivy', 'keyboard_mode', 'systemanddock')
switch_auth = []
profile_name = []
btn_name = []


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
        conn = sqlite3.connect('data/main.db')
        conn.text_factory = str
        c = conn.cursor()
        c.execute('PRAGMA encoding="UTF-8";')
        try:
            c.execute('SELECT name_order FROM orders')
            orders = c.fetchall()
            c.execute('SELECT order_town FROM orders')
            towns = c.fetchall()
            for order, town in zip(orders, towns):
                self.data.append(
                    {
                        "text": f'{order[0]} {town[0]}',
                        "on_release": lambda x=(order[0]): self.show_full_information(x)
                    }
                )
        except:
            sm.current = 'error'

    def show_full_information(self, full_information):
        full_information_screen = sm.get_screen('fullinformation')
        conn = sqlite3.connect('data/main.db')
        conn.text_factory = str
        c = conn.cursor()
        c.execute('PRAGMA encoding="UTF-8";')
        c.execute(f'SELECT * FROM orders WHERE orders.name_order = ?', (full_information,))
        information = c.fetchone()
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

        sm.current = 'fullinformation'
        # We need to change to full information screen here

    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"

    def on_leave(self):
        self.data.clear()


class RegBad(Screen):
    pass


class Registration(Screen):
    def reg(self):
        conn = sqlite3.connect('data/main.db')
        conn.text_factory = str
        c = conn.cursor()
        c.execute('PRAGMA encoding="UTF-8";')
        c.execute('''CREATE TABLE IF NOT EXISTS user
            (login text, password text, name_STO text, oblast_STO text, town_STO text, phone_number text ) ''')
        login = (str(self.ids.name.text)).casefold()
        c.execute("SELECT COUNT(login) FROM user WHERE user.login=?", (login,))
        user = c.fetchone()
        name_sto = str(self.ids.name_STO.text)
        oblast = (str(self.ids.name_obl.text)).capitalize()
        town_STO = (str(self.ids.name_town.text)).capitalize()
        """c.execute("SELECT COUNT(oblast) FROM country WHERE country.oblast=?", (oblast,))
        obl = c.fetchone()
        c.execute("SELECT COUNT(town) FROM country WHERE country.town=?", (town_STO,))
        town = c.fetchone()"""
        phone_number = (str(self.ids.number_phone.text))
        if """obl[0] != 0""" and len(name_sto) != 0 and """town[0] != 0""" and len(phone_number) != 0:
            if user[0] != 1:
                if self.ids.name_pwd.text == self.ids.name_pwd2.text:
                    hash_pwd = hashlib.sha224((self.ids.name_pwd.text).encode('utf-8')).hexdigest()
                    c.execute(
                        "INSERT INTO user(login, password, name_STO, oblast_STO, town_STO, phone_number) VALUES (?, ?, ?, ?, ?, ?)",
                        (login, hash_pwd, name_sto, oblast, town_STO, phone_number))
                    self.ids.name.text = ''
                    self.ids.name_pwd.text = ''
                    self.ids.name_pwd2.text = ''
                    self.ids.name_STO.text = ''
                    self.ids.name_obl.text = ''
                    self.ids.name_town.text = ''
                    self.ids.number_phone.text = ''
                    conn.commit()
                    return 'reggood'
                else:
                    return 'regbad'
            else:
                return 'badlog'
        else:
            return 'badobltown'


class RegGood(Screen):
    pass


class BadLogin(Screen):
    pass


class BadOblastOrTown(Screen):
    pass


class BadOblastOrTown2(Screen):
    pass


class Authorization(Screen):
    def auth(self):
        auth_pass = hashlib.sha224((self.ids.auth_pwd.text).encode('utf-8')).hexdigest()
        conn = sqlite3.connect('data/main.db')
        conn.text_factory = str
        c = conn.cursor()
        try:
            auth_name = (str(self.ids.auth_name.text)).casefold()
            c.execute(f'SELECT "password" FROM user WHERE login = "{auth_name}" ')
            hash_pwd = c.fetchone()
            if auth_pass == hash_pwd[0]:
                switch_on()
                profile_name.append(auth_name)
                self.ids.auth_name.text = ''
                self.ids.auth_pwd.text = ''
                return 'authgood'
            else:
                pass
        except:
            return 'authbad'


class ListSto(Screen):
    data = ListProperty()

    def on_pre_enter(self, *args):
        conn = sqlite3.connect('data/main.db')
        conn.text_factory = str
        c = conn.cursor()
        c.execute('PRAGMA encoding="UTF-8";')
        try:
            c.execute('SELECT name_STO FROM user')
            name_STO = c.fetchall()
            c.execute('SELECT town_STO FROM user')
            town_STO = c.fetchall()
            c.execute('SELECT phone_number FROM user')
            phone_number = c.fetchall()
            if len(name_STO) != 0:
                for i in range(len(name_STO)):
                    name_ST = name_STO[i]
                    town_ST = town_STO[i]
                    phone = phone_number[i]
                    self.data.append({"text": f'{name_ST[0]} {town_ST[0]} {phone[0]}'})
            else:
                pass
        except:
            sm.current = 'error'

    def menu(self):
        self.data.clear()
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class CreateOrder(Screen):
    def create(self):
        conn = sqlite3.connect('data/main.db')
        conn.text_factory = str
        c = conn.cursor()
        c.execute('PRAGMA encoding="UTF-8";')
        c.execute('''CREATE TABLE IF NOT EXISTS orders
            (name_order text, text_order text, order_town text, order_oblast text, order_car text, order_car_model text, order_car_year text, order_car_fuel text, order_username text, order_phone ) ''')
        name_ord = (str(self.ids.name_order.text)).capitalize()
        text_order = (str(self.ids.text_order.text)).casefold()
        order_town = (str(self.ids.order_town.text)).capitalize()
        order_obl = (str(self.ids.order_obl.text)).capitalize()
        order_car = (str(self.ids.order_car.text)).casefold()
        order_car_model = (str(self.ids.order_car_model.text)).casefold()
        order_car_year = (str(self.ids.order_car_year.text)).casefold()
        order_car_fuel = (str(self.ids.order_car_fuel.text)).casefold()
        order_username = (str(self.ids.order_username.text))
        order_phone = (str(self.ids.order_username_phone.text))
        numb = c.execute('SELECT "name_order" FROM orders').fetchall()
        number = len(numb) + 1
        name_order = f'{number}. {name_ord}'
        """c.execute("SELECT COUNT(oblast) FROM country WHERE country.oblast=?", (order_obl,))
        obl = c.fetchone()
        c.execute("SELECT COUNT(town) FROM country WHERE country.town=?", (order_town,))
        town = c.fetchone()"""
        if len(name_order) != 0 and len(text_order) != 0 and """obl[0] != 0 and town[0] != 0""" and len(
                order_car) != 0 and len(order_car_model) != 0 and len(order_car_year) != 0 and len(
            order_car_fuel) != 0 and len(order_username) != 0 and len(order_phone) != 0:
            c.execute(
                "INSERT INTO orders(name_order, text_order, order_town, order_oblast, order_car, order_car_model, "
                "order_car_year, order_car_fuel, order_username, order_phone  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name_order, text_order, order_town, order_obl, order_car, order_car_model, order_car_year,
                 order_car_fuel, order_username, order_phone))
            conn.commit()
            self.ids.name_order.text = ''
            self.ids.text_order.text = ''
            self.ids.order_town.text = ''
            self.ids.order_obl.text = ''
            self.ids.order_car.text = ''
            self.ids.order_car_model.text = ''
            self.ids.order_car_year.text = ''
            self.ids.order_car_fuel.text = ''
            self.ids.order_username.text = ''
            self.ids.order_username_phone.text = ''
            return "ordergood"
        else:
            return 'badobltown2'

    def back(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class AuthGood(Screen):
    pass


class AuthBad(Screen):
    pass


class AuthMenu(Screen):
    def exit(self):
        switch_off()
        return "menu"


class OrderGood(Screen):
    def menu(self):
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class MyProfile(Screen):
    sto_name = StringProperty()
    sto_town = StringProperty()
    sto_phone = StringProperty()

    def on_pre_enter(self):
        conn = sqlite3.connect('data/main.db')
        conn.text_factory = str
        c = conn.cursor()
        c.execute('PRAGMA encoding="UTF-8";')
        c.execute(f'SELECT name_STO, town_STO, phone_number FROM user WHERE login = "{profile_name[0]}" ')
        name_sto = c.fetchone()
        self.sto_name = name_sto[0]
        self.sto_town = name_sto[1]
        self.sto_phone = name_sto[2]


class Error(Screen):
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
sm.add_widget(Registration(name='registration'))
sm.add_widget(RegBad(name='regbad'))
sm.add_widget(RegGood(name='reggood'))
sm.add_widget(BadLogin(name='badlog'))
sm.add_widget(BadOblastOrTown(name='badobltown'))
sm.add_widget(BadOblastOrTown2(name='badobltown2'))
sm.add_widget(Authorization(name='authorization'))
sm.add_widget(ListSto(name='liststo'))
sm.add_widget(CreateOrder(name='createorder'))
sm.add_widget(AuthGood(name='authgood'))
sm.add_widget(AuthBad(name='authbad'))
sm.add_widget(AuthMenu(name='authmenu'))
sm.add_widget(OrderGood(name='ordergood'))
sm.add_widget(MyProfile(name='myprofile'))
sm.add_widget(FullInformation(name='fullinformation'))
sm.add_widget(Error(name='error'))


class MyApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()
