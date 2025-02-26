# ivw/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

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

    path('programs/', views.program_list, name='program_list'),
    path('programs/new/', views.program_create, name='program_create'),
    path('programs/edit/<int:pk>/', views.program_update, name='program_update'),

    path('demands/', views.demand_list, name='demand_list'),
    path('demands/new/', views.demand_create, name='demand_create'),
    path('demands/edit/<int:pk>/', views.demand_update, name='demand_update'),
    path('demands/analyze_i/<int:pk>/', views.demand_analysis_i, name='demand_analysis'),
    path('demands/analyze_ii/<int:pk>/', views.demand_analysis_ii, name='demand_analysis_ii'),

    path('funnel/', views.demand_funnel, name='demand_funnel'),
    path('funnel/demand/<int:pk>/', views.demand_detail, name='demand_detail'),
    path('funnel/conclude/', views.conclude_funnel, name='conclude_funnel'),
    path('funnel/finalize/', views.finalize_funnel, name='finalize_funnel'),
    path('save_changes/', views.save_changes, name='save_changes'),
    path('update_status/', views.update_status, name='update_status'),

    path('planning/', views.planning_list, name='planning_list'),
    path('planning/demand/<int:demand_id>/planning_detail/', views.planning_demand_detail, name='planning_demand_detail'),
    path('planning/demand/<int:demand_id>/action_plans/', views.action_plan_list, name='action_plan_list'),
    path('planning/demand/<int:demand_id>/action_plans/create/', views.action_plan_create, name='action_plan_create'),
    path('planning/demand/<int:demand_id>/action_plans/<int:pk>/update/', views.action_plan_update, name='action_plan_update'),
    path('planning/demand/<int:demand_id>/finalize_planning/', views.finalize_planning, name='finalize_planning'),
    path('planning/complete_prioritization/', views.complete_prioritization, name='complete_prioritization'),

    

]