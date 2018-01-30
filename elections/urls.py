from django.urls import path, re_path
from . import views

app_name = 'elections'
urlpatterns = [
    path('', views.index, name = 'home'),
    re_path(r'^areas/(?P<area>.+)/$', views.areas),
    re_path(r'^areas/(?P<area>.+)/results$', views.results),
    re_path(r'^polls/(?P<poll_id>\d+)/$', views.polls),
    re_path(r'^candidates/(?P<name>.+)/$', views.candidates),
]