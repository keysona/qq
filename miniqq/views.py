from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignupForm,LoginForm
from .models import User,Friend
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def signup(requests):
    if requests.method == 'POST':
        form = SignupForm(requests.POST)
        if form.is_valid():
            print(form.cleaned_data)
            data = form.cleaned_data
            user = User(name=data['name'],password=data['password'],address=data['address'],
                        hometown=data['hometown'],sex=data['sex'],birth=data['birth'],
                        desc=data['desc'],imageid=data['imageid'],email=data['email'])
            user.save()
            return JsonResponse({'account':user.account,'state':'success','message':'注册成功'})
        else:
            return JsonResponse({'state':'fail','message':'数据格式不对'})
    return JsonResponse({'state':'fail','message':'请用POST方法提交'})

@csrf_exempt
def login(requests):
    if requests.method == 'POST':
        form = LoginForm(requests.POST)
        if form.is_valid():
            try:
                print("帐号",requests.POST.get("account"))
                print("密码",requests.POST.get("password"))
                user = User.objects.all().get(account=int(requests.POST.get('account')))
            except ObjectDoesNotExist as e:
                return JsonResponse({'state':'fail','message':'账户或者密码错误'})
            if user.password == form.cleaned_data['password']:
                user.ip = requests.META['REMOTE_ADDR']
                user.is_login = True
                print(user.ip)
                return JsonResponse({'state':'success','message':'登录成功'})
            return JsonResponse({'state':'fail','message':'账户或者密码错误'})
        return JsonResponse({'state':'fail','message':'数据格式不对'})
    return JsonResponse({'state':'fail','message':'请用POST方法提交'})

@csrf_exempt
def get_friends(requests):
    if requests.method == 'POST':
        try:
            account = requests.POST.get("account")
            user = User.objects.get(account=account)
            result = {}
            groupname = []
            for friend in user.friends.all():
                if friend.groupname not in result.keys():
                    result[friend.groupname] = []
                    groupname.append(friend.groupname)
                temp = user_to_dict(friend.person)
                result[friend.groupname].append(temp)
            a = dict(groupname=groupname,friends=result)
            return JsonResponse(a)
        except ObjectDoesNotExist as e:
            return JsonResponse({'state':'fail','message':'不再此账户'})
    return JsonResponse({'state':'fail','message':'请用POST方法提交'})

@csrf_exempt
def add_friend(requests):
    if requests.method == 'POST':
        try:
            self_account = requests.POST.get("self_account")
            friend_account = requests.POST.get("friend_account")
            groupname = requests.POST.get("groupname")
            if self_account == friend_account:
                return JsonResponse({'state':'fail1','message':'不能添加自己'})
            self_user = User.objects.get(account=int(self_account))
            friend_user = User.objects.get(account=int(friend_account))
            if not self_user.friends.filter(person=friend_user):
                friend = Friend(groupname=groupname,person=friend_user)
                friend.save()
                self_user.friends.add(friend)
                return JsonResponse({"state":"success",'message':'添加成功'})
            else:
                return JsonResponse({"state":"fail","message":"重复添加"})
        except ObjectDoesNotExist as e:
            return JsonResponse({'state':'fail1','message':'帐号错误'})
    return JsonResponse({'state':'fail','message':'请用POST方法提交'})

@csrf_exempt
def delete_friend(requests):
    if requests.method == 'POST':
        try:
            self_account = requests.POST.get("self_account")
            friend_account = requests.POST.get("friend_account")
            if self_account == friend_account:
                return JsonResponse({'state':'fail1','message':'不能删除自己'})
            self_user = User.objects.get(account=int(self_account))
            friend_user = User.objects.get(account=int(friend_account))
            for friend in self_user.friends.all():
                if friend.person == friend_user:
                    friend.delete()
                    return JsonResponse({"state":"success","message":"删除成功"})
            return JsonResponse({"state":"success","message":"没有这位好友"})
        except ObjectDoesNotExist as e:
            return JsonResponse({'state':'fail1','message':'帐号错误'})
    return JsonResponse({'state':'fail','message':'请用POST方法提交'})

@csrf_exempt
def move_friend(requests):
    if requests.method == 'POST':
        try:
            self_account = requests.POST.get("self_account")
            friend_account = requests.POST.get("friend_account")
            groupname = requests.POST.get("groupname")
            if self_account == friend_account:
                return JsonResponse({'state':'fail1','message':'不能移动自己'})
            self_user = User.objects.get(account=int(self_account))
            friend_user = User.objects.get(account=int(friend_account))
            temp = self_user.friends.get(person=friend_user)
            temp.groupname = groupname
            temp.save()
            return JsonResponse({"state":"success","message":"移动成功"})
        except ObjectDoesNotExist as e:
            return JsonResponse({'state':'fail1','message':'帐号错误'})
    return JsonResponse({'state':'fail','message':'请用POST方法提交'})

@csrf_exempt
def find_friend(requests):
    if requests.method == 'POST':
        command = requests.POST.get("command")
        if command == 'account':
            return find_friend_to_account(requests)
        elif command == 'name':
            return find_friend_to_name(requests)
        else:
            return JsonResponse({"state":"fail","message":"参数错误"})
    return JsonResponse({'state':'fail','message':'请用POST方法提交'})

@csrf_exempt
def get_account_data(requests):
    if requests.method == 'POST':
        account = requests.POST.get("account")
        try:
            user = User.objects.get(account=int(account))
            return JsonResponse({"state":"success","message":"success",'result':user_to_dict(user)})
        except ObjectDoesNotExist as e:
            return JsonResponse({"state":"fail","message":"没有这个帐号"})
    return JsonResponse({'state':'fail','message':'请用POST方法提交'})

@csrf_exempt
def set_account_data(requests):
    if requests.method == 'POST':
        try:
            account = requests.POST.get("account")
            key = requests.POST.get("key")
            value = requests.POST.get("value")
            user = User.objects.get(account=int(account))
            setattr(user,key,value)
            user.save()
            return JsonResponse({"state":"success","message":"修改成功"})
        except ObjectDoesNotExist as e:
            return JsonResponse({"state":"fail","message":"修改失败"})
        except Exception as e:
            return JsonResponse({"state":"fail","message":"字段名错误,或者字段格式有问题"})

def find_friend_to_account(requests):
    account = requests.POST.get("account")
    try:
        return JsonResponse({"state":"success","message":"查找成功",
                            'result':user_to_dict(User.objects.get(account=int(account)))})
    except ObjectDoesNotExist as e:
        return JsonResponse({"state":"fail","message":"查找失败"})

def find_friend_to_name(requests):
    name = requests.POST.get("name")
    users = User.objects.filter(name__contains=name)
    result = []
    for user in users:
        result.append(user_to_dict(user))
    print(result)
    return JsonResponse({"state":"success","message":"查找成功",'result':result})

def user_to_dict(user):
    temp = user.__dict__
    del temp['_state']
    temp['ip'] = temp['ip'] if temp['ip'] else "";
    temp['ip_local'] = temp['ip_local'] if temp['ip_local'] else ""
    temp['android_ip'] = temp['android_ip'] if temp['android_ip'] else ""
    return temp
