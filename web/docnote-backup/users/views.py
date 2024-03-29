from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from users.models import Users
# Create your views here.
def loginPage(request):
    return render_to_response("login.html")

def login(request):
    try:
        realpwd=Users.objects.get(username=request.POST['username']).password
        if request.POST['password']==realpwd:
            request.session['user']=Users.objects.get(username=request.POST['username']).username
            return HttpResponseRedirect("/index/")
        else:
            return render_to_response("login.html",{"error_wrongpwd":True})
    except Users.DoesNotExist:
        return render_to_response("login.html",{"error_nouser":True,"info_username":request.POST['username']})



def registerPage(request):
    return render_to_response("register.html")

def register(request):
    name=request.POST['username']
    try:
        user = Users.objects.get(username=name,)
    except Users.DoesNotExist:
        tempUser=Users(
            username=request.POST['username'],
            password=request.POST['password'],
        )
        tempUser.save()
        return render_to_response("login.html",{'message_regsuccess':True})
    else:
        return render_to_response("register.html",{'message_userexist':True})




