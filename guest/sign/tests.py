from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User


# Create your tests here.
class Modules(TestCase):

    def setUp(self):
        Event.objects.create(id=3,name="oneplus 3 event",status = True,limit=2000,address='beijing',start_time='2020-04-02 00:00:00')
        Guest.objects.create(id=1,event_id=3,realname='maimai',phone='15227105153',email='15227105153@mail.com',sign=False)

    def test_event_modules(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address,"hanzhou")
        self.assertTrue(result.status)

    def test_guest_modules(self):
        result = Guest.objects.get(phone='15227105153')
        self.assertEqual(result.realname,'maimai')
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    '''测试index登录页面'''
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')


class LoginActionTest(TestCase):
    '''测试登录动作'''
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')

    def test_add_admin(self):
        #测试添加用户
        user = User.objects.get(username = "admin")
        self.assertEqual(user.username ,'admin')
        self.assertEqual(user.email,'admin@mail.com')

    def test_login_action_username_password_null(self):
        #用户名密码为空
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b"username or password error",response.content)

    def test_login_action_username_password_error(self):
        #用户名密码错误
        test_data = {'username':'admin','password':'123'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b"username or password error",response.content)

    def test_login_action_success(self):
        #登录成功
        test_data = {'username':'admin','password':'admin123456'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,302)

class EventMangeTest(TestCase):
    '''发布会管理'''
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        Event.objects.create(name='xiaomi5',limit=2000,address='beijing',status=1,start_time='2020-04-02 12:00:00')
        self.login_user={'username':'admin','password':'admin123456'}

    def test_event_mange_success(self):
        '''测试发布会'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"xiaomi5",response.content)
        self.assertIn(b"beijing",response.content)

    def test_event_mange_sreach_success(self):
        '''测试发布会搜索'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/search_name/',{"name":"xiaomi5"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"xiaomi5",response.content)
        self.assertIn(b"beijing",response.content)


class GuestManageTest(TestCase):
    '''嘉宾管理'''
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        Event.objects.create(id=1,name='xiaomi5',limit=2000,address='beijing',status=1,start_time='2020-04-02 12:00:00')
        Guest.objects.create(realname = 'maimai',phone=15227105153,email='maimai@mail.com',sign=0,event_id=1)
        self.login_user = {'username':'admin','password':'admin123456'}

    def test_event_mange_success(self):
        '''测试嘉宾信息'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"maimai",response.content)
        self.assertIn(b"15227105153",response.content)

    def test_guest_manage_search_success(self):
        '''测试嘉宾搜索'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/search_phone/',{"phone":"15227105153"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"maimai",response.content)
        self.assertIn(b"15227105153",response.content)

class SignIndexActionTest(TestCase):
    '''发布会签到'''
    def setUp(self):
        User.objects.create_user('admin','admin@main.com','admin123456')
        Event.objects.create(id=1,name="xiaomi5",limit=2000,address='beijing',status=1,start_time='2020-04-02 12:00:00')
        Event.objects.create(id=2,name="oneplus4",limit=2000,address='shenzhen',status=1,start_time='2020-04-01 12:00:00')
        Guest.objects.create(realname='alen',phone=18600000000,email='alen@mail.com',sign=0,event_id=1)
        Guest.objects.create(realname='una',phone=18600000001,email='una@mail.com',sign=1,event_id=2)
        self.login_user = {'username':'admin','password':'admin123456'}

    def test_sign_index_action_phone_null(self):
        '''手机号为空'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{"phone":''})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"phone error",response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        '''手机号或发布会id错误'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/2/',{"phone":"18600000000"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"event id or phone error",response.content)

    def test_sign_index_action_user_sign_has(self):
        '''用户已签到'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/2/',{"phone":"18600000001"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"user has sign in",response.content)

    def test_sign_index_action_sign_success(self):
        '''签到成功'''
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{"phone":"18600000000"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"sign in success",response.content)





if __name__ == "__main__":
	unittest.main()


