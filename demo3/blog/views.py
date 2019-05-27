from django.shortcuts import render,get_object_or_404,reverse,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Article,Category,Tag,Ads as AdsModel
from django.views.generic import View
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail,send_mass_mail
import markdown

from django.core.paginator import Paginator

# Create your views here.


def index(request):

    pagenum=request.GET.get('page')
    pagenum=1 if pagenum==None else pagenum
    #得到集合
    articles=Article.objects.all().order_by('-views')

    paginator=Paginator(articles,1)

    page=paginator.get_page(pagenum)

    page.parms='/'

    return render(request,'index.html',{'page':page})

def detail(request,id):
    article=get_object_or_404(Article,pk=id)
    # print(article)
    # article.body=markdown.markdown(article.body,extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc'
    # ])
    article.views+=1
    article.save()
    mk=markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ])
    article.body=mk.convert(article.body)

    article.toc=mk.toc


    return render(request,'single.html',locals())


def archives(request,year,month):
    pagenum=request.GET.get('page')
    pagenum= 1 if pagenum == None else pagenum

    articles=Article.objects.filter(create_time__year=year,create_time__month=month)
    paginator=Paginator(articles,1)

    page=paginator.get_page(pagenum)
    page.parms='/archives/%s/%s/'%(year,month)
    return render(request,'index.html',{'page':page})

def category(request,id):
    pagenum=request.GET.get('page')
    pagenum=1 if pagenum==None else pagenum

    articles=get_object_or_404(Category,pk=id).article_set.all()
    paginator=Paginator(articles,1)
    page=paginator.get_page(pagenum)
    page.parms = '/category/%s/'%(id,)
    return render(request,'index.html',{'page':page})



def tag(request,id):
    pagenum=request.GET.get('page')
    pagenum=1 if pagenum==None else pagenum

    articles=get_object_or_404(Tag,pk=id).article_set.all()
    paginator=Paginator(articles,1)
    page=paginator.get_page(pagenum)
    page.parms='/tag/%s/'%(id,)
    return render(request,'index.html',{'page':page})

class Contacts(View):

    def get(self,request):

        cf = ContactForm()


        return render(request,'contact.html',locals())
    def post(self,request):
        try:
            send_mail('测试邮件。。。', '可以发送邮件', settings.DEFAULT_FROM_EMAIL, ["1327870569@qq.com"])
        except Exception as e:
            print(e)

        cf = ContactForm(request.POST)
        cf.save()
        cf = ContactForm()

        return render(request,'contact.html',{'info':'成功','cf':cf})

# def contacts(request):
#
#     return render(request, 'contact.html')

class Ads(View):
    def get(self,request):
        return render(request,"addads.html")

    def post(self,request):
        img = request.FILES["img"]
        desc = request.POST.get("desc")
        ad = AdsModel(img = img, desc= desc)
        ad.save()
        return redirect(reverse('blog:index'))