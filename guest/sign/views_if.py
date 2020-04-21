from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db.utils import IntegrityError
import time

#添加发布会接口
def add_event(request):
    eid = request.POST.get('eid','')
    name = request.POST.get('name','')
    limit = request.POST.get('limit','')
    status = request.POST.get('status','')
    address = request.POST.get('address','')
    start_time = request.POST.get('start_time','')

    if eid == '' or name == '' or limit == '' or status == '' or address == '' or start_time == '':
        return JsonResponse({'status':10021,'message':'参数为空'})

    result = Event.objects.filter(id = eid)
    if result:
        return JsonResponse({'status':10022,'message':'发布会ID已存在'})

    result = Event.objects.filter(name = name)
    if result:
        return JsonResponse({'status':10023,'message':'发布会名称已存在'})
    if status == '':
        status =1

    try:
        Event.objects.create(id=eid,name=name,limit=limit,status=int(status),address=address,start_time=start_time)
    except ValidationError as e:
        error = '开始时间格式错误'
        return JsonResponse({'status':10024,'message':error})

    return JsonResponse({'status':200,'message':'添加成功'})

#查询发布会
def get_event_list(request):
    eid = request.GET.get("eid","")  #发布会ID
    name = request.GET.get("name","")

    if eid == '' and name == '':
        return JsonResponse({'status':10021,'message':'参数错误'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id = eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'query result is 空的'})
        else:
            event['name']=result.name
            event['limit']=result.limit
            event['status']=result.status
            event['address']=result.address
            event['start_time']=result.start_time
            return JsonResponse({'status':200,'message':'success','data':event})

    if name !='':
        datas = []
        results = Event.objects.filter(name__contain=name)
        if results:
            for r in results:
                event=[]
                event['name']=r.name
                event['limit']=r.limit
                event['status']=r.status
                event['address']=r.address
                event['start_time']=r.start_time
                datas.append(event)
            return JsonResponse({'status':200,'message':'success','data':datas})

        else:
            return JsonResponse({'status':10022,'message':'无搜索结果'})

#添加嘉宾接口
def add_guest(request):
    eid = request.POST.get('eid','')
    realname = request.POST.get('realname','')
    phone = request.POST.get('phone','')
    email = request.POST.get('email','')

    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status':10021,'message':'参数错误'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'发布会id为空'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023,'message':'发布会还未开始'})

    event_limit = Event.objects.get(id = eid).limit
    guest_limit = Guest.objects.filter(event_id = eid) #发布会已添加的嘉宾个数

    if len(guest_limit) > event_limit:
        return JsonResponse({'status':10024,'message':'发布会的嘉宾多余限定值'})

    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)
    if n_time >= e_time:
        return JsonResponse({'status':10025,'message':'发布会已经开始了'})

    try:
        Guest.objects.create(realname=realname,phone=int(phone),email=email,sign=0,event_id = int(eid))
    except IntegrityError:
        return JsonResponse({'status':10026,'message':'手机号已存在，无法添加'})
    return JsonResponse({'status':200,'message':'success add'})

#查询嘉宾接口
def get_guest_list(request):
    eid = request.GET.get('eid','')
    phone = request.GET.get('phone','')

    if eid == '':
        return JsonResponse({'status':10021,'message':'发布会ID为空'})

    if eid != '' and phone == '':
        datas=[]
        result = Guest.objects.filter(event_id = eid)
        if result:
            for r in result:
                guest={}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse({'status':200,'message':'success','data':datas})
        else:
            return JsonResponse({'status':10022,'message':'查询结果为空'})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(event_id = eid,phone = phone)
            print(result)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'查询结果为空'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status':200,'message':'success','data':guest})

#嘉宾签到接口
def user_sign(request):
    phone = request.POST.get('phone','')
    eid = request.POST.get('eid','')

    if eid == '' or phone == '':
        return JsonResponse({'status':10021,'message':'参数为空'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'发布会ID不存在'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023,'message':'发布会暂未发布，无法签到'})

    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime,"%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if e_time <= n_time:
        return JsonResponse({'status':10024,'message':'发布会已结束'})

    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status':10025,'message':'嘉宾信息不存在'})

    result = Guest.objects.filter(event_id = eid,phone=phone)
    if not result:
        return JsonResponse({'status':10026,'message':'此发布会无该嘉宾信息'})

    result = Guest.objects.get(event_id=eid,phone=phone).sign
    if result:
        return JsonResponse({'status':10027,'message':'嘉宾已签到'})
    else:
        Guest.objects.filter(event_id=eid,phone=phone).update(sign=1)
        return JsonResponse({'status':200,'message':'sign success'})