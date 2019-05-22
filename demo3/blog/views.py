from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Article
import markdown
# Create your views here.


def index(request):

    pagenum=request.GET.get('page')
    print('1',pagenum)
    pagenum=1 if pagenum==None else pagenum
    #得到集合
    articles=Article.objects.all().order_by('-views')

    paginator=Paginator(articles,1)

    page=paginator.get_page(pagenum)

    return render(request,'index.html',{'page':page})

def detail(request,id):
    article=get_object_or_404(Article,pk=id)
    # print(article)
    # article.body=markdown.markdown(article.body,extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc'
    # ])

    mk=markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ])
    article.body=mk.convert(article.body)

    article.toc=mk.toc

    return render(request,'single.html',locals())
