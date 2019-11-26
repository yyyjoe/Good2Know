from django.conf.urls import url
from django.conf.urls import include
from Good2Know import views

urlpatterns = [
    #url(r'^$',views.index,name='index'),
    #url(r'^formpage/',views.form_name_view,name='form_name'),
    url(r'^$', views.getLDA, name='urlname'),
]