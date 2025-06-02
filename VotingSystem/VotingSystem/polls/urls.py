# polls/urls.py
from django.urls import path
from . import views
from django.contrib import admin

app_name = 'polls'  # This adds a namespace for the polls app

urlpatterns = [
    path('', views.login_view, name='login'),  # Login view
    path('index/', views.index, name='index'),  # Index view
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('list/', views.polls_list, name='polls_list'),  # Polls list page
    path('poll/<int:poll_id>/vote/', views.vote, name='vote'),  # Vote on a specific poll
    path('poll/<int:poll_id>/results/', views.poll_results, name='poll_results'),  # Poll results page
]

