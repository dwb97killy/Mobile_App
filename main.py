from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from pathlib import Path
from datetime import datetime
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import random, json, glob



'''改成名人名言'''



Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current = "signup_scr"
        print("Sign up button pressed")
    def log_in(self, username, password):
        with open("users.json") as file:
            users = json.load(file)
        if username in users and users[username]["password"] == password:
            self.manager.transition.direction = "left"
            self.manager.current = "login_scr_succ"
        else:
            self.ids.info_err.text = "Information Error!"


class SignupScreen(Screen):
    def add_user(self, username, password):
        with open("users.json") as file:
            users = json.load(file)
            print(username, password)
        users[username] = {'username': username, 'password': password, 'create': datetime.now().strftime('%Y-%m-%d %H-%M-%S')}
        with open("users.json", "w") as file:
            json.dump(users, file)
        self.manager.current = "signup_scr_succ"
    def back_log_in(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_scr"

class SignupScreenSuccess(Screen):
    def back_log_in(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_scr"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_scr"

    def get_file(self, input):
        print(input)
        input = input.lower()
        print(input)
        available_feelings = glob.glob("Files/*txt")
        available_feelings = [Path(filename).stem for filename in available_feelings]
        if input in available_feelings:
            with open(f"Files/{input}.txt") as file:
                quotes = file.readlines()
            self.ids.show_text.text = random.choice(quotes)
        else:
            self.ids.show_text.text = "Try another name please"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_scr"


class RootWidget(ScreenManager):
    pass


class MainAPP(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainAPP().run()

