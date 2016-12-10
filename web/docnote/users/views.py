from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .models import Users,SortTree,Docs
# Create your views here.

def getUserID(request):
    try:
        userid = request.session['user']
        if userid == None:
            return None
        else:
            return userid
    except:
        return None

def loginPage(request):
    return render_to_response("users/login.html")

def newclass(request):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})
    
    fatherid=request.POST['fatherid']
    newname=request.POST['newname']

    if fatherid=='-1':
        tempST=SortTree(
            parendid=0,
            key="",
            level=1,
            owner=userid,
            value=newname,
            pathvalue=newname,
        )
        tempST.save()


    else:

        father = SortTree.objects.get(id=fatherid)
    
        tempST=SortTree(
            parendid=fatherid,
            key=father.key+fatherid+"-",
            level=father.level+1,
            owner=userid,
            value=newname,
            pathvalue=father.pathvalue+"-"+newname,
        )

        tempST.save()
    return HttpResponseRedirect("/index/")



treeinfo={}
html=""
ddata={}
def gao(xid):
    global html,treeinfo,ddata
    html+="<li>"
    html+="\n<span><i class=\"icon-leaf\"></i>"+ddata[xid].value+"</span><a href=""> Gose somwhere</a>"
    if xid in treeinfo:
        html+="<ul>"
        for yid in treeinfo[xid]:
            gao(yid)
        html+="</ul>"
    html+="</li>"
    return
    

def makehtml(classList):
    global html,treeinfo,ddata
    treeinfo={}
    ddata={}
    for i in range(len(classList)):
        ddata[classList[i].id]=classList[i]
    for x in classList:
        if x.parendid in treeinfo:
            treeinfo[x.parendid]+=[x.id]
        else:
            treeinfo[x.parendid]=[x.id]
   
    html="<ul>"
    for x in classList:
        if x.level==1:
            gao(x.id)
    html+="</ul>"
    return html

def indexPage(request):
    userid=getUserID(request)
    if userid==None:
        return render_to_response("users/login.html",{'error_notlogin':True})

    classList = SortTree.objects.filter(owner=userid).order_by("pathvalue")
    tablehtml = makehtml(classList)
    docList = Docs.objects.filter(owner=userid).order_by("-id")
    
    return render_to_response("users/index.html",{'classList':classList,'tablehtml':tablehtml,'docList':docList})






def login(request):
    try:
        realpwd=Users.objects.get(username=request.POST['username']).password
        if request.POST['password']==realpwd:
            request.session['user']=Users.objects.get(username=request.POST['username']).id
            return HttpResponseRedirect("/index/")
        else:
            return render_to_response("users/login.html",{"error_wrongpwd":True})
    except Users.DoesNotExist:
        return render_to_response("users/login.html",{"error_nouser":True,"info_username":request.POST['username']})



def registerPage(request):
    return render_to_response("users/register.html")

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
        return render_to_response("users/login.html",{'message_regsuccess':True})
    else:
        return render_to_response("users/register.html",{'message_userexist':True})


