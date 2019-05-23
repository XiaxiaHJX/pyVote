from django.shortcuts import render,get_object_or_404,reverse,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Article,Category,Tag
from django.views.generic import View
from .forms import ContactForm
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
        cf = ContactForm(request.POST)
        cf.save()
        cf = ContactForm()
        return render(request,'contact.html',{'info':'成功','cf':cf})