from selenium import webdriver


class LoginPage(object):
    client = None

    def __init__(self, c):
        self.client = c

    @property
    def title(self):
        return self.client.title

    def set_user_name(self, name):
        user_input = self.client.find_element_by_name('username')
        user_input.send_keys(name)

    def set_pwd(self, pwd):
        pwd_input = self.client.find_element_by_name('password')
        pwd_input.send_keys(pwd)

    def submit(self):
        submit = self.client.find_element_by_name('submit')
        submit.click()
