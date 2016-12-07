from django.conf.urls import patterns, include, url
from django.contrib import admin
from docnote import settings
from users import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'docnote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.loginPage),
    url(r'^login/$',views.login),
    url(r'^register/$',views.registerPage),
    url(r'^reg/$',views.register),
    


    url(r'^site_medias/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS, 'show_indexes': True}),
)
