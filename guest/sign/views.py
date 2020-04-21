from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def index(request):
 #   return HttpResponse("Hello Django!")
    return render(request,"index.html")

#登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
#调用Django认证登录
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
#        if username == 'admin' and password == 'admin123':
#            return HttpResponse('login success')
#标准            return HttpResponseRedirect('/event_manage/')
#使用cookies
            response = HttpResponseRedirect('/event_manage/')
#            response.set_cookie('user',username,3600)
#使用session
            request.session['user'] = username
            return response
        else:
            return render(request,'index.html',{'error':'username or passowrd error'})


#登录后重定向到发布会管理页
@login_required
def event_manage(request):
#    return render(request,'event_manage.html')
#使用cookies
#    username = request.COOKIES.get('user','')
#使用session
    username = request.session.get('user','')
    event_list = Event.objects.all()
    return render(request,"event_manage.html",{"user":username,"events":event_list})

#搜索
@login_required
def search_name(request):
    username=request.session.get('user','')
    search_name = request.GET.get("name",'')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})

#嘉宾表
@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()

    paginator=Paginator(guest_list,3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        #如果page不在范围，取最后一页面
        contacts=Paginator.page(paginator.num_pages)


    return render(request,"guest_manage.html",{"user":username,"guests":contacts})


#签到页面
@login_required
def sign_index(request,event_id):
    event = get_object_or_404(Event,id = event_id)
    return render(request,'sign_index.html',{'event':event})

#签到动作
@login_required
def sign_index_action(request,event_id):

    event = get_object_or_404(Event, id=event_id)
    phone =  request.POST.get('phone','')

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.'})

    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.'})

    result = Guest.objects.get(event_id = event_id,phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in."})
    else:
        Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
            'guest': result
            })

'''
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid),
    phone = request.POST.get('phone',''),
    print(phone)

 #   result = Guest.objects.filter(phone=phone)
#    if not result:
#        return render(request,'sign_index.html',{'event':event,'hint':'phone error'})

    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':result})

    result = Guest.objects.filter(phone=phone,event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'用户已经签到了'})
    else:
        Guest.objects.filter(phone=phone,event_id = eid).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':登录成功,'guest':result})
'''

#退出登录
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response