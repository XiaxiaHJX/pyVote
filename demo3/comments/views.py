from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Comment
from blog.models import Article
import markdown

# Create your views here.

def comment(request,id):
    if request.method=='GET':
        return render(request, 'single.html')
    elif request.method=='POST':
        blog=Article.objects.get(pk=id)
        rev=Comment()
        rev.username=request.POST.get('name')
        print(rev.username)
        rev.email=request.POST.get('email')
        rev.url=request.POST.get('url')
        rev.content=request.POST.get('comment')
        rev.article=blog
        rev.save()
        return HttpResponseRedirect('/detail/%s/'%(id,))


