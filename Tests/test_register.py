# -*- coding: utf-8 -*-

# @Time    : 2020/12/2 下午5:35
# @Author  : cyq
# @File    : test_register.py


import unittest
import requests
class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:5000//api/userOpt'

    def tearDown(self) -> None:
        pass

    def test_register_err_username(self):
        usernameEmp= ""
        usernameNUm =1233
        password="12312432"
        res  = requests.post(url = self.url,json={"username":usernameEmp,"password":password})
        self.assertEqual(res.json()['code'],1)
        self.assertEqual(res.json()['err'],"请正确传参")
        res  = requests.post(url = self.url,json={"password":password})
        self.assertEqual(res.json()['code'],1)
        self.assertEqual(res.json()['err'],"请正确传参")
        res  = requests.post(url = self.url,json={"username":usernameNUm,"password":password})
        print(res.json())
        self.assertEqual(res.json()['code'],1)
        self.assertEqual(res.json()['err'],"请正确传参")
if __name__ == '__main__':
    main = unittest.main()
    