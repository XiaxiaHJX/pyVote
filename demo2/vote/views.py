from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader,RequestContext
from .models import VoteHeadline,VoteOption_1,VoteUser
from .util import checklogin
from django.views.generic import View
# Create your views here.

# def login(request):
#     username=request.session.get(key=username)
def register(request):
    if request.method=='GET':
        return render(request, 'vote/register.html')
    elif request.method=='POST':
        user=VoteUser()
        user.name=request.POST['name']
        name=request.POST['name']
        user.pwd=request.POST['pwd']
        # print(VoteUser.objects.all().filter(name=name))
        if VoteUser.objects.all().filter(name=name):
            return render(request, 'vote/register.html',{'register':'改账号已注册'})
        else:
            user.save()
            return HttpResponseRedirect('/vote/index/')

def login(request):
    if request.method == 'GET':
        return render(request,'vote/login.html')
    else:
        username=request.POST.get('name')
        print(username)
        pwd=request.POST.get('pwd')
        print(VoteUser.objects.all().filter(name=username).filter(pwd=pwd))
        if username != None and VoteUser.objects.all().filter(name=username).filter(pwd=pwd):
            res=redirect(reverse('vote:index'))
            request.session['username']=username
            request.session['pwd'] = pwd
            return res
        else:
            return render(request,'vote/login.html',{'error':'用户错误'})

def logout(request):
    res=redirect(reverse('vote:login'))
    request.session.flush()
    return res

@checklogin
def index(request):
    username=request.session.get('username')
    titlelist=VoteHeadline.objects.all()
    return render(request, 'vote/index.html',locals())

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

def result(request,id):
    optionlist = VoteHeadline.objects.get(pk=id)
    return render(request, 'vote/result.html', locals())




