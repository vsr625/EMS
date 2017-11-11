from django.conf.urls import url

from EMS import views

uuid_pattern = '[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}'

urlpatterns = [
    url(r'^$', views.homepage_view, name='home'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^login_a/$', views.login_a_view, name='login_a'),
    url(r'^login_p/$', views.login_p_view, name='login_p'),
    url(r'^login_c/$', views.login_c_view, name='login_c'),
    url(r'^dashboard_a/$', views.dashboard_a_view, name='dashboard_a'),
    url(r'^dashboard_p/$', views.dashboard_p_view, name='dashboard_p'),
    url(r'^dashboard_c/$', views.dashboard_c_view, name='dashboard_c'),
    url(r'^dashboard_a/create_event$', views.create_event_view, name='create_event'),
    url(r'^dashboard_a/create_co$', views.create_co_view, name='create_co'),
    url(
        r'^dashboard_a/update_event/(?P<event_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})',
        views.update_event, name='update_event'),
    url(
        r'^dashboard_a/delete_event/(?P<event_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})',
        views.delete_event, name='delete_event'),
    url(
        r'^dashboard_a/view_event/(?P<event_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})',
        views.view_event, name='view_event'),
    url(r'^dashboard_a/create_faculty$', views.create_faculty_view, name='create_faculty'),
    url(r'^dashboard_a/create_sp$', views.create_sp_view, name='create_sp'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^dashboard_p/(?P<event_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})',
        views.register_event_view, name='register_event'),
    url(
        r'^dashboard_c/update_winner/(?P<event_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})',
        views.update_winner, name='update_winner'),
    url(r'^generate/(?P<event_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})',
        views.generate_view, name='generate')
]
