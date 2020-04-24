#-*-coding: utf-8 -*- 

import requests
import unittest

class GetEventListTest(unittest.TestCase):
    '''查询发布会接口'''
    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    def test_get_event_null(self):
        '''发布会ID为空'''
        r = requests.get(self.url, params={'eid':''})
        result = r.json()
        self.assertEqual(result['status'],10021)
        self.assertEqual(result['message'],'参数错误')

    def test_get_event_error(self):
        '''发布会不存在'''
        r = requests.get(self.url,params={'eid':'199'})
        result = r.json()
        self.assertEqual(result['status'],10022)
        self.assertEqual(result['message'],'query result is 空的')

    def test_get_event_success(self):
        '''查询成功'''
        r = requests.get(self.url,params={'eid':'1'})
        result = r.json()
        self.assertEqual(result['status'],200)
        self.assertEqual(result['message'],"success")
        self.assertIn(result['data']['name'],'小白生日会aa')
        self.assertEqual(result['data']['address'],'望京')
        self.assertEqual(result['data']['start_time'],'2020-03-02T06:16:37')

class GetGuestListTest(unittest.TestCase):
    '''查询嘉宾'''
    def setUp(self):
        self.url="http://127.0.0.1:8000/api/get_guest_list/"

    def test_get_guestevent_null(self):
        '''发布会ID为空'''
        r = requests.get(self.url,params={'eid':''})
        result = r.json()
        self.assertEqual(result['status'],10021)
        self.assertEqual(result['message'],'发布会ID为空')

    def test_get_guestcz_null(self):
        '''发布会ID存在，嘉宾手机号为空'''
        r = requests.get(self.url,params={'eid':'3','phone':''})
        result = r.json()
        self.assertEqual(result['status'],200)
        self.assertEqual(result['message'],'success')

    def test_get_guest_null(self):
        '''发布会ID不存在'''
        r = requests.get(self.url,params={'eid':'199'})
        result = r.json()
        self.assertEqual(result['status'],10022)
        self.assertEuqal(result['message'],'查询结果为空')

    def test_get_guest_notnull(self):
        '''发布会ID存在，嘉宾手机号存在'''
        r = requests.get(self.url, params={'eid': '3','phone':'15227105153'})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEuqal(result['message'], 'success')

    def test_get_guest_error(self):
        '''发布会ID存在，嘉宾手机号不存在'''
        r = requests.get(self.url, params={'eid': '3','phone':'1521153'})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEuqal(result['message'], '查询结果为空')


if __name__ == '__main__':
    unittest.main()