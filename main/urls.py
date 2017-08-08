from django.conf.urls import url

from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^search/', views.search, name='search'),
    url(r'^about/', views.about, name='about'),
    url(r'^activity/', views.activity_all, name='activity_all'),
    url('^profile/(?P<username>[a-zA-Z0-9_]+)', views.profile, name='profile'),
    url('^activity/(?P<username>[a-zA-Z0-9_]+)', views.activity, name='activity'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^posts/', views.posts, name='posts'),
    url(r'^post/(?P<id>P[0-9]+)', views.post, name='post'),

]
