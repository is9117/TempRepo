# -*- coding: utf-8 -*-

from mycafe.tests import CommonAPITest

from account.factory import AccountFactory
from menu.factory import ProductFactory

class AccountViewTest(CommonAPITest):
    
    def test_점장_회원가입(self):

        self.client.token = None    # API client logout

        phone_num_stub = ''.join([str(self.faker.random_digit()) for _ in range(8)])
        phone_num = f'010{phone_num_stub}'
        password = self.faker.password()

        url = '/api/v1/account'
        data = {
            'phone_num': phone_num, 
            'password': password
        }
        res = self.client.post(url, data)
        self.assert201(res)
        res_data = res.json()

        self.assertEqual(res_data['meta']['code'], 201)
        self.assertEqual(res_data['data']['phone_num'], phone_num)
        self.assertTrue('password' not in res_data['data'])

class TokenViewTest(CommonAPITest):
        
    def __signed_up(self):
        password = self.faker.password()
        account = AccountFactory(plaintext_password=password)
        return account.phone_num, password

    def setUp(self) -> None:
        self.phone_num, self.password = self.__signed_up()
        return super().setUp()
    
    def test_로그인(self):

        url = '/api/v1/token'
        data = {
            'phone_num': self.phone_num,
            'password': self.password
        }
        res = self.client.post(url, data)
        self.assert201(res)
        token = res.json()['data']
        self.assertIsNotNone(token)
        self.assertTrue(isinstance(token, str))

        # 새로운 토큰 생성
        res = self.client.post(url, data)
        self.assert201(res)
        new_token = res.json()['data']
        self.assertIsNotNone(new_token)
        self.assertNotEqual(token, new_token)

    def test_로그아웃(self):

        self.client.login(self.phone_num, self.password)
        token = self.client.token
        self.assertIsNotNone(token)
        self.assertTrue(isinstance(token, str))

        # login test
        product = ProductFactory()
        url = f'/api/v1/products/{product.id}'
        res = self.client.get(url)
        self.assert200(res)

        data = {'token': self.client.token}
        res = self.client.delete('/api/v1/token', data)
        self.assert204(res)

        # logout test
        product = ProductFactory()
        url = f'/api/v1/products/{product.id}'
        res = self.client.get(url)
        self.assert401(res)
