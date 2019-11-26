from django.shortcuts import render
from . import forms
from . import LDA_API
from django.http import JsonResponse
from django.http import HttpResponse
from . import user_account
# Create your views here.

LDA = LDA_API.LDA()

def index(request):
    my_dict = {'insert_content':"This is message"}
    return render(request,'Good2Know/index.html',context=my_dict)

def getLDA(request):
    user_id = request.GET['user_id']
    text = user_account.get_user_post(user_id,10)
    data = LDA.getLDA(text)
    #do something with this user
    return HttpResponse(data)

    #form = forms.FormName()
    #return render(request,'Good2Know/form_page.html',{'form':form})
