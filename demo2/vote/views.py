from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader,RequestContext
from .models import VoteHeadline,VoteOption_1,MyUser
from .util import checklogin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as lgi,logout as lgo
from django.core.mail import send_mail,send_mass_mail,EmailMultiAlternatives
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired
from django.shortcuts import render
from django.http import HttpResponse
# 引入绘图模块
from PIL import Image, ImageDraw, ImageFont
import random, io


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
        email=request.POST.get('email')
        # print(username,pwd,pwd1)
        errors=None
        if pwd != pwd1:
            errors='密码不一致'
            return render(request,'vote/login.html',{'errors':errors})
        else:
            user=MyUser.objects.create_user(username=username,password=pwd)
            user.is_active=False
            user.save()
            #得到序列化工具
            serutil=Serializer(settings.SECRET_KEY)
            #使用工具对字典对象序列化
            result=serutil.dumps({'userid':user.id}).decode('utf-8')

            mail=EmailMultiAlternatives('点击激活用户','<a href="http://127.0.0.1:8000/vote/active/%s/">点击激活</a>'%(result,),settings.DEFAULT_FROM_EMAIL,[email])

            mail.content_subtype='html'
            mail.send()
            return render(request,'vote/login.html',{'error':'请在一小时内激活'})


def newpwd(request):
    if request.method=='GET':
        return render(request, 'vote/newpwd.html')
    if request.method=='POST':
        username=request.POST.get('username1')
        user = MyUser.objects.filter(username=username)
        # name=User.objects.filter(username=username)
        if user:
            pwd=request.POST.get('pwd1')
            pwd1=request.POST.get('pwd2')
            if pwd == pwd1:
                user.password=pwd
                # user.save()
                return render(request,'vote/newpwd.html',{"str":"更改成功"})
        else:
            return HttpResponse('更改失败，没有该账号')



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
        verifycode=request.POST.get('verify')
        if verifycode == request.session.get('verifycode'):
            # user=authenticate(request,username=username,password=pwd)
            user = get_object_or_404(MyUser, username=username)
            if not user.is_active:
                return render(request, 'vote/login.html', {"error": "用户名尚未激活"})
            else:
                check = user.check_password(pwd)
                if check:
                    lgi(request, user)
                    return redirect(reverse('vote:index'))
                else:
                    return render(request, 'vote/login.html', {'error': '用户或者密码错误'})

            # print(user)
            # if user:
            #     lgi(request,user)
            #     return redirect(reverse('vote:index'))
            # else:
            #     return render(request,'vote/login.html',{"error": "用户名或者密码错误"})
        else:
            return render(request,'vote/login.html',{'error':'验证码错误'})

def active(request,info):
    serutil=Serializer(settings.SECRET_KEY)
    try:
        obj=serutil.loads(info)
        id=obj['userid']
        user=get_object_or_404(MyUser,pk=id)
        user.is_active=True
        user.save()
        return  redirect(reverse('vote:login'))
    except SignatureExpired as e:
        return HttpResponse('过期了')



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

# def verify(request,):
#     #构造验证码
#
#     # Create your views here.
#     def login(request):
#         if request.method == "GET":
#             return render(request, 'verifycodetest/login.html')
#         elif request.method == "POST":
#             username = request.POST["username"]
#             password = request.POST["password"]
#             verifycode = request.POST["verifycode"]
#             if verifycode == request.session["verifycode"]:
#                 return HttpResponse("登录成功")
#             else:
#                 return HttpResponse("验证码错误")

def verify(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100),
               random.randrange(20, 100),
               random.randrange(20, 100))
    width = 100
    heigth = 35
    # 创建画面对象
    im = Image.new('RGB', (width, heigth), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, heigth))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('cambriab.ttf', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    request.session['verifycode'] = rand_str
    f = io.BytesIO()
    im.save(f, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(f.getvalue(), 'image/png')

def checkuser(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        print(username)

        if MyUser.objects.filter(username=username).first():
            print('if:',username)
            return JsonResponse({'state':1})

        else:
            print(username)
            return JsonResponse({'state':0,'error':'用户不存在'})
