from django.conf.urls import url

from . import views

app_name = 'discussions'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>Q[0-9]+)$', views.question, name='question'),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^answer/(?P<question_id>Q[0-9]+)$', views.answer, name='answer'),
    url(r'^delete/(?P<id>[AQ][0-9]+)', views.delete, name='delete'),
    url(r'^edit/(?P<id>[AQ][0-9]+)', views.edit, name='edit'),
    url(r'^confirm/(?P<id>[AQ][0-9]+)', views.confirm, name='confirm'),
    url(r'^vote/', views.vote, name='vote'),
]
