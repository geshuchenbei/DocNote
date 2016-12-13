from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from .models import Users,SortTree,Docs
import time
import urllib.request
import os
from zipfile import *
import shutil
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

def getnowtime():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    return time.strftime(ISOTIMEFORMAT,time.localtime())


def setreadA(request,num='1'):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    tempDoc=Docs.objects.get(id=num,owner=userid)
    tempDoc.readstatus="已粗读"
    tempDoc.readlog+="\n"+getnowtime()+"\n修改阅读状态为 已粗读"
    tempDoc.save()
    return HttpResponseRedirect("/docdetail/"+num+"/")

def setreadB(request,num='1'):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    tempDoc=Docs.objects.get(id=num,owner=userid)
    tempDoc.readstatus="已精读"
    tempDoc.readlog+="\n"+getnowtime()+"\n更新阅读状态为 已精读"
    tempDoc.save()
    return HttpResponseRedirect("/docdetail/"+num+"/")
    
def updateStatus(request,num='1'):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    tempDoc=Docs.objects.get(id=num,owner=userid)
    tempDoc.readstatus=request.POST['newdocstatus']
    tempDoc.readlog+="\n"+getnowtime()+"\n更新阅读状态为 "+request.POST['newdocstatus']
    tempDoc.save()
    return HttpResponseRedirect("/docdetail/"+num+"/")

def updateName(request,num='1'):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    tempDoc=Docs.objects.get(id=num,owner=userid)
    tempDoc.docname=request.POST['newdocname']
    tempDoc.readlog+="\n"+getnowtime()+"\n修改文献名称"
    tempDoc.save()
    return HttpResponseRedirect("/docdetail/"+num+"/")

def updateUrl(request,num='1'):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    tempDoc=Docs.objects.get(id=num,owner=userid)
    tempDoc.docurl=request.POST['newurl']
    tempDoc.readlog+="\n"+getnowtime()+"\n更新文献地址"
    tempDoc.save()
    return HttpResponseRedirect("/docdetail/"+num+"/")

def updateNode(request,num='1'):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    tempDoc=Docs.objects.get(id=num,owner=userid)
    tempDoc.treenodeid=request.POST['newfatherid']
    tempDoc.readlog+="\n"+getnowtime()+"\n修改文献分类"
    tempDoc.save()
    return HttpResponseRedirect("/docdetail/"+num+"/")

def updateNote(request,num='1'):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    tempDoc=Docs.objects.get(id=num,owner=userid)
    tempDoc.usernote=request.POST['newnote']
    tempDoc.readlog+="\n"+getnowtime()+"\n更新笔记"
    tempDoc.save()
    return HttpResponseRedirect("/docdetail/"+num+"/")

def delDoc(request,num='1'):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    tempDoc=Docs.objects.get(id=num,owner=userid)
    tempDoc.delete()
    return HttpResponseRedirect("/index/")

def docupdatefile(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})
    
    tempdoc=Docs.objects.get(owner=userid,id=num)
    tempdoc.docfile=request.FILES['docfile']
    tempdoc.readlog+="\n"+getnowtime()+"\n更新文件"
    tempdoc.save()

    return HttpResponseRedirect("/docdetail/"+num)

def newdoc(request):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    ndocname=request.POST['docname']
    nreadstatus=request.POST['docstatus']
    ndocurl=request.POST['docurl']
    ntreenodeid=request.POST['doctreenodeid']
    nlogs=getnowtime()+" 添加\n"
    tempDoc=Docs(
        docname=ndocname,
        readstatus=nreadstatus,
        docurl=ndocurl,
        readlog=nlogs,
        usernote="",
        treenodeid=ntreenodeid,
        owner=userid,
        docfile=request.FILES['docfile'],
    )
    tempDoc.save()

    return HttpResponseRedirect("/index/")


def newclass(request):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})
    
    fatherid=request.POST['fatherid']
    newname=request.POST['newname']

    if fatherid=='-1':
        tempST=SortTree(
            parendid=0,
            key="-",
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
    html+="\n<span><i class=\"icon-leaf\"></i>"+ddata[xid].value+"</span>"+"<a href=\"/classdetail/"+str(xid)+"/cur\">"+" 分类详情</a>"
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


def docdetail(request,num='1'):
    #what if no such num
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})
    classList = SortTree.objects.filter(owner=userid).order_by("pathvalue")
    docInfo = Docs.objects.filter(owner=userid,id=num)
    classInfo = SortTree.objects.filter(owner=userid,id=docInfo[0].treenodeid)
    return render_to_response("users/docdetail.html",{'classList':classList,'docInfo':docInfo[0],'classInfo':classInfo[0].pathvalue})

def classcurDetail(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})
    
    classList = SortTree.objects.filter(owner=userid).order_by("pathvalue")
    tablehtml = makehtml(classList)
    curdocList = Docs.objects.filter(owner=userid,treenodeid=num)
    return render_to_response("users/treedetail.html",{'classList':classList,'tablehtml':tablehtml,'docList':curdocList,'fullDoc':False})


def classfullDetail(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})
    
    classList = SortTree.objects.filter(owner=userid).order_by("pathvalue")
    tablehtml = makehtml(classList)
    curnode = SortTree.objects.get(owner=userid,id=num)
    tempsonlist = SortTree.objects.filter(owner=userid,key__contains=curnode.key+str(curnode.id)+"-")
    fulldocList=[]
    curdocList = Docs.objects.filter(owner=userid,treenodeid=num)
    for x in curdocList:
        fulldocList.append(x)
    for x in tempsonlist:
        temp = Docs.objects.filter(owner=userid,treenodeid=x.id)
        for y in temp:
            fulldocList.append(y)
    
    return render_to_response("users/treedetail.html",{'classList':classList,'tablehtml':tablehtml,'docList':fulldocList,'fullDoc':True})

def dreplace(bstr,key,newname):
    k=bstr.split("-")
    for i in range(len(k)):
        if k[i]==key:
            k[i]=newname
    ans=""
    for x in k:
        ans+=x+"-"
    return ans[:-1]
def classnewname(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

    newname=request.POST['newclassname']
    thisclass=SortTree.objects.get(owner=userid,id=num)
    classlist=SortTree.objects.filter(owner=userid)
    for x in classlist:
        x.pathvalue=dreplace(x.pathvalue,thisclass.value,newname)
        x.save()
    thisclass=SortTree.objects.get(owner=userid,id=num)
    thisclass.value=newname
    thisclass.save()

    return HttpResponseRedirect("/classdetail/"+num+"/edit/")

def classnewfather(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})

  

    classList = SortTree.objects.filter(owner=userid).order_by("pathvalue")
    curnode = SortTree.objects.get(owner=userid,id=num)
    tempsonlist = SortTree.objects.filter(owner=userid,key__contains=curnode.key+str(curnode.id)+"-").order_by("level")
    fathernode=SortTree.objects.get(owner=userid,id=request.POST['newfatherid'])
    curnode.key=fathernode.key+str(fathernode.id)+"-"
    curnode.level=fathernode.level+1
    curnode.parendid=fathernode.id
    curnode.pathvalue=fathernode.pathvalue+"-"+curnode.value
    curnode.save()

    for x in tempsonlist:
        tempfa=SortTree.objects.get(owner=userid,id=x.parendid)
        x.key=tempfa.key+str(tempfa.id)+"-"
        x.level=tempfa.level+1
        x.pathvalue=tempfa.pathvalue+"-"+x.value
        x.save()
    
  
    return HttpResponseRedirect("/classdetail/"+num+"/edit/")


def classedit(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})
    
    classList = SortTree.objects.filter(owner=userid).order_by("pathvalue")
    tablehtml = makehtml(classList)
    classInfo = SortTree.objects.get(owner=userid,id=num)
    tempsonlist = SortTree.objects.filter(owner=userid,key__contains=classInfo.key+str(classInfo.id)+"-")
    classListB=[]
    for x in classList:
        if x not in tempsonlist:
            classListB.append(x)
    
    return render_to_response("users/treedetail.html",{'classList':classList,'tablehtml':tablehtml,'edit':True,'classInfo':classInfo,"classListB":classListB})


def classdel(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})
    
    curclass = SortTree.objects.get(owner=userid,id=num)
    tempsonlist = SortTree.objects.filter(owner=userid,key__contains=curclass.key+str(curclass.id)+"-")
    

    curdocs = Docs.objects.filter(owner=userid,treenodeid=curclass.id)
    for x in curdocs:
        x.delete()
    for x in tempsonlist:
        dellist=Docs.objecs.filter(owner=userid,treenodeid=x.id)
        for y in dellist:
            y.delete()

    curclass.delete()
    for x in tempsonlist:
        x.delete()

    return HttpResponseRedirect("/index/")

def downloadfile_standard(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})


    docinfo=Docs.objects.get(owner=userid,id=num)

    def makelogfile(fn , buf_size=262144):
        
        my_dir = 'temp/uploads/'
        for file_name in os.listdir(my_dir):
            os.remove(my_dir+file_name)
    
        f = open("temp/"+urllib.request.unquote(fn)+".log" ,"w")
        f.write(docinfo.readlog)
        f.close()

        g = open("temp/"+urllib.request.unquote(fn)+".note","w")
        g.write(docinfo.usernote)
        g.close()


        shutil.copyfile(urllib.request.unquote(fn),'temp/'+urllib.request.unquote(fn))
        truename=urllib.request.unquote(fn)[8:]



        myzip = ZipFile('tempzip', 'w', ZIP_DEFLATED) 
        for file_name in os.listdir(my_dir): 
            file_path = my_dir + file_name 
            print(file_path) 
            myzip.write(file_path,file_name) 
        myzip.close() 

        shutil.copyfile('tempzip','temp/uploads/'+truename+'.zip')
        
        



    def readFile(fn, buf_size=262144):
        f = open(urllib.request.unquote(fn), "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
  

    the_file_name = docinfo.docfile.url
    makelogfile(the_file_name)
    the_file_name="temp/"+the_file_name+'.zip'
    response = StreamingHttpResponse(readFile(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name[13:])

    return response


def downloadfile_docdetail(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})


    docinfo=Docs.objects.get(owner=userid,id=num)


  
    def readFile(fn, buf_size=262144):
        f = open(urllib.request.unquote(fn), "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
  
    the_file_name = docinfo.docfile.url
    response = StreamingHttpResponse(readFile(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name[8:])

    return response



def downloadfile_tree(request,num="1"):
    userid=getUserID(request)
    if userid==None:
        return render_to_response('users/login.html',{'error_notlogin':True})




    classList = SortTree.objects.filter(owner=userid).order_by("pathvalue")
    curnode = SortTree.objects.get(owner=userid,id=num)
    tempsonlist = SortTree.objects.filter(owner=userid,key__contains=curnode.key+str(curnode.id)+"-")
    fulldocList=[]
    curdocList = Docs.objects.filter(owner=userid,treenodeid=num)
    for x in curdocList:
        fulldocList.append((x,curnode.pathvalue))
    for x in tempsonlist:
        temp = Docs.objects.filter(owner=userid,treenodeid=x.id)
        for y in temp:
            fulldocList.append((y,x.pathvalue))


    
    my_dir = 'temp/uploads/'
    for file_name in os.listdir(my_dir):
        os.remove(my_dir+file_name)
    for x in fulldocList:
        shutil.copyfile(urllib.request.unquote(x[0].docfile.url),'temp/'+urllib.request.unquote(x[0].docfile.url)+"---$#$---"+x[1])
    

    def gao(value):
        k=value.split("---$#$---")
        ans=""
        print(k)
        temp=k[1].split('-')
        for x in temp:ans+=x+os.sep
        print(ans)
        return ans+os.sep+k[0]

    myzip = ZipFile('tempzip', 'w', ZIP_DEFLATED) 
    for file_name in os.listdir(my_dir): 
        file_path = my_dir + file_name
        print(gao(file_name))
        myzip.write(file_path,gao(file_name)) 
    myzip.close() 

    truename=curnode.pathvalue
    shutil.copyfile('tempzip','temp/uploads/'+truename+'.zip')

    print("------------------------------*******************---------------------------------")

        
  
    def readFile(fn, buf_size=262144):
        f = open(urllib.request.unquote(fn), "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
  
    the_file_name='temp/uploads/'+truename+'.zip'
    response = StreamingHttpResponse(readFile(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name[13:])

    return response



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


