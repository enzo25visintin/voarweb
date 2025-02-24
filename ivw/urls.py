# ivw/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/about', views.about, name='about'),

    path('users/', views.user_list, name='user_list'),
    path('users/new/', views.user_create, name='user_create'),
    path('users/edit/<int:pk>/', views.user_update, name='user_update'),

    path('sdgs/', views.sdg_list, name='sdg_list'),
    path('sdgs/new/', views.sdg_create, name='sdg_create'),
    path('sdgs/edit/<int:pk>/', views.sdg_update, name='sdg_update'),

    path('materiality/', views.materiality_issue_list, name='materiality_issue_list'),
    path('materiality/new/', views.materiality_issue_create, name='materiality_issue_create'),
    path('materiality/edit/<int:pk>/', views.materiality_issue_update, name='materiality_issue_update'),

    path('stakeholders/', views.stakeholder_list, name='stakeholder_list'),
    path('stakeholders/new/', views.stakeholder_create, name='stakeholder_create'),
    path('stakeholders/edit/<int:pk>/', views.stakeholder_update, name='stakeholder_update'),

    path('demands/', views.demand_list, name='demand_list'),
    path('demands/new/', views.demand_create, name='demand_create'),
    path('demands/edit/<int:pk>/', views.demand_update, name='demand_update'),
    path('demands/analyze_i/<int:pk>/', views.demand_analysis_i, name='demand_analysis'),
    path('demands/analyze_ii/<int:pk>/', views.demand_analysis_ii, name='demand_analysis_ii'),

]