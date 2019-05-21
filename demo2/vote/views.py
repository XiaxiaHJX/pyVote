from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader,RequestContext
from .models import VoteHeadline,VoteOption_1,MyUser
from .util import checklogin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as lgi,logout as lgo

from django.views.generic import View
# Create your views here.
# def login(request):
#     username=request.session.get(key=username)

# def register(request):
#     if request.method=='GET':
#         return render(request, 'vote/oldregister.html')
#     elif request.method=='POST':
#         user=VoteUser()
#         user.name=request.POST['name']
#         name=request.POST['name']
#         user.pwd=request.POST['pwd']
#         # print(VoteUser.objects.all().filter(name=name))
#         if VoteUser.objects.all().filter(name=name):
#             return render(request, 'vote/oldregister.html',{'register':'改账号已注册'})
#         else:
#             user.save()
#             return HttpResponseRedirect('/vote/login/')

def register(request):
    if request.method == 'POST':
        username=request.POST.get('username_1')
        pwd=request.POST.get('pwd_1')
        pwd1=request.POST.get('pwd_2')
        print(username,pwd,pwd1)
        errors=None
        if pwd != pwd1:
            errors='密码不一致'
            return render(request,'vote/login.html',{'errors':errors})
        else:
            MyUser.objects.create_user(username=username,password=pwd)

            return redirect(reverse('vote:login'))


def newpwd(request):
    if request.method=='GET':
        return render(request, 'vote/newpwd.html')
    if request.method=='POST':
        username=request.POST.get('username1')
        name=User.objects.filter(username=username)
        if name:
            pwd=request.POST.get('pwd1')
            pwd1=request.POST.get('pwd2')
            if pwd == pwd1:
                name.set_password(pwd)
        return render(request,'vote/newpwd.html',{"str":"更改成功"})



def login(request):
    if request.method == 'GET':
        from .forms import loginForm
        lf = loginForm()

        return render(request,'vote/login.html',{'lf':lf})
    else:
    #     username=request.POST.get('name')
    #     print(username)
    #     pwd=request.POST.get('pwd')
    #     # print(VoteUser.objects.all().filter(name=username).filter(pwd=pwd))
    #     if username != None :
    #         res=redirect(reverse('vote:index'))
    #         request.session['username']=username
    #         request.session['pwd'] = pwd
    #         return res
    #     else:
    #         return render(request,'vote/login.html',{'error':'用户错误'})
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
        print(username,pwd)

        user=authenticate(request,username=username,password=pwd)
        print(user)
        if user:
            lgi(request,user)
            return redirect(reverse('vote:index'))
        else:
            return render(request,'vote/login.html',{"error": "用户名或者密码错误"})


def logout(request):
    res=redirect(reverse('vote:login'))
    lgo(request)
    return res

@checklogin
def index(request):
    username=request.session.get('username')
    titlelist=VoteHeadline.objects.all()
    return render(request, 'vote/index.html',locals())

@checklogin
def option(request,id):
    option1 = VoteHeadline.objects.get(pk=id)
    if request.method=='GET':
        return render(request, 'vote/option.html', locals())
    elif request.method=='POST':
        oid=request.POST['oid']
        opt=VoteOption_1.objects.get(pk=oid)
        print(opt)
        opt.num+=1
        opt.save()
        return HttpResponseRedirect('/vote/result/%s/' % (id,))

@checklogin
def result(request,id):
    optionlist = VoteHeadline.objects.get(pk=id)
    return render(request, 'vote/result.html', locals())




