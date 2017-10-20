from django.conf.urls import url

from EMS import views

urlpatterns = [
    url(r'^$', views.homepage_view, name='home'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^dashboard/$', views.dashboard_view, name='dashboard'),
    url(r'^logout/$', views.logout_view, name='logout')
]
