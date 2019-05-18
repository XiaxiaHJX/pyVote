from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader,RequestContext
from .models import VoteHeadline,VoteOption_1
# Create your views here.

def index(request):
    titlelist=VoteHeadline.objects.all()
    return render(request, 'vote/index.html',{'titlelist':titlelist})

def option(request,id):
    option1 = VoteHeadline.objects.get(pk=id)
    if request.method=='GET':
        return render(request, 'vote/option.html', {'option1': option1})
    elif request.method=='POST':
        optionname=request.POST['optionname']
        opt=VoteOption_1.objects.get(optionname=optionname)
        opt.num+=1
        opt.save()
        return HttpResponseRedirect('/vote/result/%s/' % str(opt.head.id,))

def result(request,id):
    optionlist = VoteHeadline.objects.get(pk=id)
    return render(request, 'vote/result.html', {'optionlist': optionlist})




