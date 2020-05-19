import json
import requests

def test_geteventlisttest():
    '''查询发布会'''
    url = "http://127.0.0.1:8000/api/get_event_list/"
    r = requests.get(url, params={'eid': '1'})
    result = r.json()
#    print(result)
    assert result['status']==200
    assert result['data']['name']=='小白生日会'
    assert result['data']['address']=='望京'
    assert result['message']=="success"
    assert result['data']['start_time']=='2020-03-02T06:16:37'

def test_addeventlisttest():
    '''新增发布会'''
    url="http://127.0.0.1:8000/api/add_event/"
    params={'eid': '10','name': 'pytest-test2','status': '1','limit': '20','address': '地点','start_time': '2020-01-03 12:00:00'}
    r=requests.post(url,data=params)
    result=r.json()
    assert result['status']==200
    assert result['message']=="添加成功"