# coding=utf-8
import unittest
import threading
from selenium import webdriver
from app import create_app, db
from app.models import Role, User
import re
from forgery_py import internet, basic


class SeleniumTest(unittest.TestCase):
    client = None
    app_ctx = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        if cls.client:
            cls.app = create_app('testing')
            cls.app_ctx = cls.app.app_context()
            cls.app_ctx.push()

            db.drop_all()
            db.create_all()
            Role.seed()
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        cls.client.get('http://localhost:5000/shutdown')
        cls.client.close()

        db.session.remove()
        cls.app_ctx.pop()

    def setUp(self):
        if self.client is None:
            self.skipTest(u'略过测试')

    def tearDown(self):
        pass

    def test_user_login(self):
        from login_page import LoginPage
        new_user = User(name=internet.user_name(),
                        email=internet.email_address(),
                        password=basic.text())
        db.session.add(new_user)
        db.session.commit()

        page = LoginPage(self.client)
        self.client.get('http://localhost:5000/auth/login')
        self.assertTrue(u'登录' in page.title)

        page.set_user_name(new_user.name)
        page.set_pwd(new_user.password)
        page.submit()

        # 返回注册结果

        self.assertTrue(re.search(u'欢迎来到Ray的博客', self.client.page_source))
