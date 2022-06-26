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


class RegBad(Screen):
    pass


class Registration(Screen):
    def reg(self):
        try:
            cursor = connectdb().cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS users(login text, password text, name_STO text, oblast_STO text, town_STO text, phone_number text );')
            user = [0]
            login = (str(self.ids.name.text)).casefold()
            try:
                cursor.execute("SELECT COUNT(login) FROM users WHERE login LIKE %s", (login,))
                user = cursor.fetchone()
            except:
                pass
            name_sto = str(self.ids.name_STO.text)
            oblast = (str(self.ids.name_obl.text)).capitalize()
            town_STO = (str(self.ids.name_town.text)).capitalize()
            """cursor.execute("SELECT COUNT(oblast) FROM country WHERE country.oblast=?", (oblast,))
            obl = cursor.fetchone()
            cursor.execute("SELECT COUNT(town) FROM country WHERE country.town=?", (town_STO,))
            town = cursor.fetchone()"""
            phone_number = (str(self.ids.number_phone.text))
            if """obl[0] != 0""" and len(name_sto) != 0 and """town[0] != 0""" and len(phone_number) != 0:
                if user[0] != 1:
                    if self.ids.name_pwd.text == self.ids.name_pwd2.text:
                        hash_pwd = hashlib.sha224((self.ids.name_pwd.text).encode('utf-8')).hexdigest()
                        cursor.execute(
                            "INSERT INTO users(login, password, name_STO, oblast_STO, town_STO, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                            [login, hash_pwd, name_sto, oblast, town_STO, phone_number])
                        connectdb().commit()
                        self.ids.name.text = ''
                        self.ids.name_pwd.text = ''
                        self.ids.name_pwd2.text = ''
                        self.ids.name_STO.text = ''
                        self.ids.name_obl.text = ''
                        self.ids.name_town.text = ''
                        self.ids.number_phone.text = ''
                        return 'reggood'
                    else:
                        return 'regbad'
                else:
                    return 'badlog'
            else:
                return 'badobltown'
        except:
            sm.current = 'notsignal'


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
        try:
            auth_pass = hashlib.sha224((self.ids.auth_pwd.text).encode('utf-8')).hexdigest()
            cursor = connectdb().cursor()
            auth_name = (str(self.ids.auth_name.text)).casefold()
            try:
                cursor.execute("SELECT COUNT(login) FROM users WHERE login LIKE %s", (auth_name,))
                user = cursor.fetchone()
            except:
                pass
            cursor.execute(f'SELECT "password" FROM users WHERE login LIKE %s ', (auth_name,))
            hash_pwd = cursor.fetchone()
            if user[0] == 1:
                if auth_pass == hash_pwd[0]:
                    switch_on()
                    profile_name.append(auth_name)
                    self.ids.auth_name.text = ''
                    self.ids.auth_pwd.text = ''
                    connectdb().close()
                    return 'authgood'
                else:
                    return 'authbad'
            else:
                return 'authbad'
        except:
            sm.current = 'notsignal'


class ListSto(Screen):
    data = ListProperty()

    def on_pre_enter(self, *args):
        try:
            cursor = connectdb().cursor()
            try:
                cursor.execute('SELECT name_STO FROM users')
                name_STO = cursor.fetchall()
                cursor.execute('SELECT town_STO FROM users')
                town_STO = cursor.fetchall()
                cursor.execute('SELECT phone_number FROM users')
                phone_number = cursor.fetchall()
                if len(name_STO) != 0:
                    for i in range(len(name_STO)):
                        name_ST = name_STO[i]
                        town_ST = town_STO[i]
                        phone = phone_number[i]
                        self.data.append({"text": f'{name_ST[0]} {town_ST[0]} {phone[0]}'})
                else:
                    pass
            except:
                pass
            connectdb().close()
        except:
            sm.current = 'notsignal'

    def menu(self):
        self.data.clear()
        if len(switch_auth) == 1:
            return "authmenu"
        else:
            return "menu"


class CreateOrder(Screen):

    def create(self):
        try:
            cursor = connectdb().cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS orders(name_order text, text_order text, order_town text, order_oblast text, order_car text, order_car_model text, order_car_year text, order_car_fuel text, order_username text, order_phone text );')
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
            try:
                numb = cursor.execute('SELECT "name_order" FROM orders').fetchall()
                number = len(numb) + 1
            except:
                number = 1
            name_order = f'{number}. {name_ord}'
            """cursor.execute("SELECT COUNT(oblast) FROM country WHERE country.oblast=?", (order_obl,))
            obl = cursor.fetchone()
            cursor.execute("SELECT COUNT(town) FROM country WHERE country.town=?", (order_town,))
            town = cursor.fetchone()"""
            if len(name_order) != 0 and len(text_order) != 0 and """obl[0] != 0 and town[0] != 0""" and len(
                    order_car) != 0 and len(order_car_model) != 0 and len(order_car_year) != 0 and len(
                order_car_fuel) != 0 and len(order_username) != 0 and len(order_phone) != 0:
                cursor.execute(
                    "INSERT INTO orders(name_order, text_order, order_town, order_oblast, order_car, order_car_model,order_car_year, order_car_fuel, order_username, order_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    [name_order, text_order, order_town, order_obl, order_car, order_car_model, order_car_year,
                     order_car_fuel, order_username, order_phone])
                connectdb().commit()
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
        except:
            sm.current = 'notsignal'

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
        try:
            cursor = connectdb().cursor()
            cursor.execute(f'SELECT name_STO, town_STO, phone_number FROM users WHERE login LIKE %s', (profile_name[0],))
            name_sto = cursor.fetchone()
            self.sto_name = name_sto[0]
            self.sto_town = name_sto[1]
            self.sto_phone = name_sto[2]
        except:
            sm.current = 'notsignal'


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
sm.add_widget(NoSignal(name='notsignal'))


class MyApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()
