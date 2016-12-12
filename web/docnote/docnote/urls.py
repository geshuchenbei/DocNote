"""docnote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from users import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.loginPage),
    url(r'^login/$',views.login),
    url(r'^register/$',views.registerPage),
    url(r'^reg/$',views.register),
    url(r'^index/$',views.indexPage),
    url(r'^newclass/$',views.newclass),
	url(r'^newdoc/$',views.newdoc),
	url(r'^docdetail/(?P<num>[0-9]+)/$',views.docdetail),
	url(r'^setreadA/(?P<num>[0-9]+)/$',views.setreadA),
	url(r'^setreadB/(?P<num>[0-9]+)/$',views.setreadB),
	url(r'^updatestatus/(?P<num>[0-9]+)/$',views.updateStatus),
	url(r'^updatename/(?P<num>[0-9]+)/$',views.updateName),
	url(r'^updatelink/(?P<num>[0-9]+)/$',views.updateUrl),
	url(r'^updatenode/(?P<num>[0-9]+)/$',views.updateNode),
	url(r'^updatenote/(?P<num>[0-9]+)/$',views.updateNote),
	url(r'^deldoc/(?P<num>[0-9]+)/$',views.delDoc),
	url(r'^classdetail/(?P<num>[0-9]+)/cur/$',views.classcurDetail),
	url(r'^classdetail/(?P<num>[0-9]+)/full/$',views.classfullDetail),
	url(r'^classdetail/(?P<num>[0-9]+)/edit/$',views.classedit),
	url(r'^classdetail/(?P<num>[0-9]+)/edit/newname$',views.classnewname),
	url(r'^classdetail/(?P<num>[0-9]+)/edit/newfather$',views.classnewfather),
	url(r'^classdetail/(?P<num>[0-9]+)/edit/del$',views.classdel),

]
