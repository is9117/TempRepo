# -*- coding: utf-8 -*-

from mycafe.tests import CommonAPITest

from account.factory import AccountFactory
from menu.factory import ProductFactory
from menu.models import Product
from menu.serializers import ProductSerislizer

class ProductViewTest(CommonAPITest):

    def __signed_up(self):
        password = self.faker.password()
        account = AccountFactory(plaintext_password=password)
        return account.phone_num, password

    def setUp(self) -> None:
        self.phone_num, self.password = self.__signed_up()
        self.client.login(self.phone_num, self.password)
        return super().setUp()
    
    def test_상품등록(self):

        url = '/api/v1/products'
        data = ProductSerislizer(ProductFactory.build()).data

        exist = Product.objects.filter(category=data['category']).exists()
        self.assertFalse(exist)

        res = self.client.post(url, data)
        self.assert201(res)
        res_data = res.json()

        self.assertEqual(res_data['data']['category'], data['category'])
        self.assertEqual(res_data['data']['price'], data['price'])
        self.assertEqual(res_data['data']['cost'], data['cost'])
        self.assertEqual(res_data['data']['name'], data['name'])
        self.assertEqual(res_data['data']['description'], data['description'])
        self.assertEqual(res_data['data']['barcode'], data['barcode'])
        self.assertEqual(res_data['data']['expiration_date'], data['expiration_date'])
        self.assertEqual(res_data['data']['size'], data['size'])
        
        exist = Product.objects.filter(category=data['category']).exists()
        self.assertTrue(exist)

    def test_상품등록_실패(self):
        url = '/api/v1/products'
        ori_data = ProductSerislizer(ProductFactory.build()).data

        exist = Product.objects.filter(category=ori_data['category']).exists()
        self.assertFalse(exist)

        data = dict(ori_data)
        data['category'] = (-100,)
        res = self.client.post(url, data)
        self.assert400(res)

        data = dict(ori_data)
        data['price'] = 'a'
        res = self.client.post(url, data)
        self.assert400(res)

        data = dict(ori_data)
        data['cost'] = True
        res = self.client.post(url, data)
        self.assert400(res)

        data = dict(ori_data)
        data['name'] = [1,2,3]
        res = self.client.post(url, data)
        self.assert400(res)

        data = dict(ori_data)
        data['description'] = {'a': 1}
        res = self.client.post(url, data)
        self.assert400(res)

        data = dict(ori_data)
        data['barcode'] = [1,2,3]
        res = self.client.post(url, data)
        self.assert400(res)

        data = dict(ori_data)
        data['expiration_date'] = 'test'
        res = self.client.post(url, data)
        self.assert400(res)

        data = dict(ori_data)
        data['size'] = 'M'
        res = self.client.post(url, data)
        self.assert400(res)

    def test_수정(self):

        product = ProductFactory()
        
        # PUT
        data = ProductSerislizer(product).data
        new_name = self.faker.name()
        self.assertNotEqual(new_name, data['name'])
        data['name'] = new_name
        url = f'/api/v1/products/{product.id}'
        res = self.client.put(url, data)
        self.assert200(res)
        res_data = res.json()
        self.assertEqual(res_data['data']['name'], new_name)
        product.refresh_from_db()
        self.assertEqual(product.name, new_name)

        # PATCH
        data = {'category': self.faker.word()}
        self.assertNotEqual(product.category, data['category'])
        url = f'/api/v1/products/{product.id}'
        res = self.client.patch(url, data)
        self.assert200(res)
        res_data = res.json()
        self.assertEqual(res_data['data']['category'], data['category'])
        product.refresh_from_db()
        self.assertEqual(product.category, data['category'])

    def test_삭제(self):

        product = ProductFactory()
        inst_id = product.id

        inst = Product.objects.get(pk=inst_id)
        self.assertIsNotNone(inst)

        url = f'/api/v1/products/{inst_id}'
        res = self.client.delete(url)
        self.assert204(res)

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=inst_id)

    def test_리스트조회(self):

        for _ in range(5):
            ProductFactory()

        url = '/api/v1/products'
        res = self.client.get(url)
        self.assert200(res)
        res_data = res.json()

        self.assertEqual(len(res_data['data']['results']), 5)
    
    def test_커서_리스트(self):

        for _ in range(15):
            ProductFactory()

        url = '/api/v1/products'
        res = self.client.get(url)
        self.assert200(res)
        res_data = res.json()

        self.assertEqual(len(res_data['data']['results']), 10)
        self.assertIsNotNone(res_data['data']['next'])

        url = res_data['data']['next']
        res = self.client.get(url)
        self.assert200(res)
        res_data = res.json()

        self.assertEqual(len(res_data['data']['results']), 5)
        self.assertIsNone(res_data['data']['next'])

    def test_조회(self):

        product = ProductFactory()

        url = f'/api/v1/products/{product.id}'
        res = self.client.get(url)
        self.assert200(res)
        res_data = res.json()
        data = res_data['data']

        self.assertEqual(product.category, data['category'])
        self.assertEqual(product.price, data['price'])
        self.assertEqual(product.cost, data['cost'])
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.description, data['description'])
        self.assertEqual(product.barcode, data['barcode'])
        self.assertEqual(product.expiration_date, data['expiration_date'])
        self.assertEqual(product.size, data['size'])
        
    def test_초성_생성(self):

        url = '/api/v1/products'
        data = ProductSerislizer(ProductFactory.build()).data
        data['name'] = '슈크림 라때'

        res = self.client.post(url, data)
        self.assert201(res)
        res_data = res.json()
        inst_id = res_data['data']['id']

        inst = Product.objects.get(pk=inst_id)
        self.assertEqual(inst.name_chosungs, 'ㅅㅋㄹㄹㄸ')

        data = {'name': '아이스 아메리카노'}
        url = f'/api/v1/products/{inst_id}'
        res = self.client.patch(url, data)
        self.assert200(res)
        inst.refresh_from_db()
        self.assertEqual(inst.name_chosungs, 'ㅇㅇㅅㅇㅁㄹㅋㄴ')

    def test_쿼리(self):

        Product.objects.all().delete()

        url = '/api/v1/products'
        data = ProductSerislizer(ProductFactory.build()).data
        data['name'] = '슈크림 라때'
        res = self.client.post(url, data)
        self.assert201(res)
        res_data = res.json()
        inst_id = res_data['data']['id']

        def success(keyword):
            url = f'/api/v1/products?query={keyword}'
            res = self.client.get(url)
            self.assert200(res)
            res_data = res.json()
            data = res_data['data']['results'][0]
            self.assertEqual(data['id'], inst_id)

        success('슈크림')
        success('크림')
        success('라때')
        success('ㅅㅋㄹ')
        success('ㅋㄹ')
        success('ㄹㄸ')

        def fail(keyword):
            url = f'/api/v1/products?query={keyword}'
            res = self.client.get(url)
            self.assert200(res)
            res_data = res.json()
            self.assertEqual(len(res_data['data']['results']), 0)

        fail('크림슈')
        fail('때라')
        fail('ㄹㅋㅅ')
        fail('ㅇㅇ')
